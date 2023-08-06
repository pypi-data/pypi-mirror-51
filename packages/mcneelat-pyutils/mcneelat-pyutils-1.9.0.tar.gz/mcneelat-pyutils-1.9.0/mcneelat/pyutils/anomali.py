from datetime import datetime as dt, timedelta
from mcneelat.pyutils.confutils import AbstractLogUtils
import requests


class ThreatStream(AbstractLogUtils):
    """Class containing handy methods common to working with the Anomali ThreatStream API."""

    """Map of general IOC categories to the most interesting IOC types."""
    ICATEGORY_MAP = {
        "domain": "apt_domain,c2_domain,exfil_domain,exploit_domain,mal_domain",
        "ip": "apt_ip,c2_ip,exfil_ip,exploit_ip,mal_ip",
        "url": "apt_url,c2_url,exfil_url,exploit_url,mal_url"
    }

    def __init__(self, api_user, api_key, min_confidence=50, last_modified_days=90,
                 results_limit=0, verbose=True):
        """
        Initialize class.
        :param api_user: API username
        :param api_key: API secret key
        :param min_confidence: minimum confidence for IOCs to look for
        :param last_modified_days: number of days ago IOCs must have been modified in order to include in results
        :param results_limit: limit of results from API queries; 0 = unlimited
        :param verbose: whether or not to print log messages
        """
        self.next_url_base = None
        self.base_url = "https://api.threatstream.com"
        self.intel_url_part = "/api/v2/intelligence/"
        self.creds_url_part = "username=%s&api_key=%s" % (api_user, api_key)
        self.min_confidence = min_confidence
        self.last_modified_days = last_modified_days
        self.results_limit = results_limit
        self.set_confidence(min_confidence)
        AbstractLogUtils.__init__(self, verbose)

    def set_confidence(self, min_confidence):
        """
        Set minimum confidence level.
        :param min_confidence: minimum confidence level on a scale of 0 to 100
        :return: None
        """
        self.min_confidence = min_confidence
        self.next_url_base = "%s?%s&status=active&confidence__gte=%i&limit=%i" % (
            self.intel_url_part, self.creds_url_part, self.min_confidence, self.results_limit
        )

    def is_threat(self, test_object):
        """
        Check if an indicator is malicious (i.e. an active IOC in ThreatStream)
        :param test_object: indicator to check
        :return: True if malicious, False if not found active in ThreatStream
        """
        self.log('[*] Checking if object %s is a threat...' % test_object)
        result = self.get_ioc_details(test_object)
        return result is not None

    def get_ioc_details(self, test_object):
        """
        Get details for one specific IOC.
        :param test_object: object to search for
        :return: list of dictionaries (usually only one in the list) containing IOC details
        """
        last_modified = (dt.today() - timedelta(days=self.last_modified_days)).strftime("%Y-%m-%dT00:00:00Z")
        next_url = "%s&modified_ts__gte=%s&value=%s" % (self.next_url_base, last_modified, test_object)
        self.log("[*] Searching for details on object %s..." % test_object)
        try:
            json_data = requests.get(self.base_url + next_url).json()
        except ValueError:
            return None
        try:
            json_data.get('objects')[0]
        except:
            return None
        return json_data.get('objects')

    def get_iocs(self, icategory, severity="high"):
        """
        Get a list of IOCs and their details from a specified category.
        :param icategory: domain, ip, or url
        :param severity: low, medium, high, very-high
        :return: list of IOCs and their details
        """
        last_modified = (dt.today() - timedelta(days=self.last_modified_days)).strftime("%Y-%m-%dT00:00:00Z")
        next_url = "%s&modified_ts__gte=%s&meta.severity__gte=%s&itype=%s" % (
            self.next_url_base, last_modified, severity, ThreatStream.ICATEGORY_MAP[icategory]
        )
        self.log("[*] Starting to gather IOCs...")
        results = []
        while next_url is not None and next_url != "null":
            try:
                json_data = requests.get(self.base_url + next_url).json()
            except ValueError:
                self.log("Warning, call to URL '%s' resulted in no JSON object response." % self.base_url + next_url)
                break
            results.extend(json_data.get('objects'))
            next_url = json_data.get('meta').get('next')
        return results
