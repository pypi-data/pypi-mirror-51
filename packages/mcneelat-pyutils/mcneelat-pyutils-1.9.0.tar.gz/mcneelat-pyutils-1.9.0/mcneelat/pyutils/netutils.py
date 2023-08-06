import re


class PyNetAddr:
    """This is a pure Python implementation of the Perl module NetAddr::IP."""

    ip_re = r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'
    mask_values = [0, 128, 192, 224, 240, 248, 252, 254, 255]

    def __init__(self, address, mask=None):
        """
        Initialize class.
        :param address: single IP address, or address and mask in CIDR notation (i.e. 10.0.0.0/24)
        :param mask: subnet mask in full notation (i.e. 255.255.255.0); None if address param is in CIDR notation
        """
        self.address, self.broadcast, self.cidr_mask, self.mask, self.network, self.range = (
            None, None, None, None, None, None)
        if not self.set_new(address, mask):
            raise ValueError('Invalid address or subnet mask!')

    @staticmethod
    def is_valid_addr(address):
        """
        Check if this is a valid IP address or network.
        :param address: IP address or network
        :return: True if valid, False if not
        """
        if re.search(PyNetAddr.ip_re, address):
            splitter = address.split('.')
            for i in range(0, len(splitter)):
                tmp_i = int(splitter[i])
                if i == 0 and tmp_i == 0:
                    return False
                if tmp_i < 0 or tmp_i > 255:
                    return False
            return True
        return False

    @staticmethod
    def is_valid_mask(mask):
        """
        Check if this is a valid subnet mask.
        :param mask: subnet mask in full notation (i.e. 255.255.255.0)
        :return: True if valid, False if not
        """
        if re.search(PyNetAddr.ip_re, mask):
            splitter = mask.split('.')
            for i in range(0, len(splitter)):
                tmp_i = int(splitter[i])
                if tmp_i not in PyNetAddr.mask_values:
                    return False
                # check for next octet as <= current
                if i > 0 and tmp_i > int(splitter[i - 1]):
                    return False
            # PyNetAddr.calc_cidr_mask(mask)
            return True
        return False

    @staticmethod
    def calc_network(address, mask):
        """
        Calculate the network address from the set IP address and subnet mask.
        :param address: IP address
        :param mask: subnet mask
        :return: network address
        """
        addr_splitter = address.split('.')
        mask_splitter = mask.split('.')
        network_arr = []
        for i in range(0, len(addr_splitter)):
            network_arr.append(str(int(addr_splitter[i]) & int(mask_splitter[i])))
        return '.'.join(network_arr)

    @staticmethod
    def calc_broadcast(address, mask):
        """
        Calculate the broadcast address from the set IP address and subnet mask.
        :param address: IP address
        :param mask: subnet mask
        :return: broadcast address
        """
        network = PyNetAddr.calc_network(address, mask)
        network_splitter = network.split('.')
        mask_splitter = mask.split('.')
        i = len(mask_splitter) - 1
        breaker = False
        while i >= 0 and not breaker:
            network_octet = format(int(str(bin(int(network_splitter[i])))[2:], 2),
                                   '{fill}{width}b'.format(width=8, fill=0))
            mask_octet = format(int(str(bin(int(mask_splitter[i])))[2:], 2), '{fill}{width}b'.format(width=8, fill=0))

            j = len(mask_octet) - 1
            tmp_octet = list(network_octet)
            while j >= 0:
                if mask_octet[j] == '0':
                    tmp_octet[j] = '1'
                elif mask_octet[j] == '1':
                    breaker = True
                    break
                j -= 1

            network_splitter[i] = str(int(''.join(tmp_octet), 2))
            i -= 1
        return '.'.join(network_splitter)

    @staticmethod
    def calc_range(network, broadcast):
        """
        Calculate the range of addresses in the subnet.
        :param network: network address
        :param broadcast: broadcast address
        :return: range of addresses in subnet
        """
        return network + " - " + broadcast

    @staticmethod
    def calc_cidr_mask(mask):
        """
        Calculate the CIDR mask from the given full notation subnet mask.
        :param mask: full notation subnet mask (i.e. 255.255.255.0)
        :return: subnet mask in CIDR notation (i.e. /24)
        """
        mask_splitter = mask.split('.')
        cidr_mask = 0
        for i in range(0, len(mask_splitter)):
            mask_octet = format(int(str(bin(int(mask_splitter[i])))[2:], 2), '{fill}{width}b'.format(width=8, fill=0))
            cidr_mask += mask_octet.count('1')
        return cidr_mask

    @staticmethod
    def calc_full_mask(cidr_mask):
        """
        Calculate the full subnet mask from the given CIDR mask.
        :param cidr_mask: CIDR mask bits
        :return: full notation subnet mask
        """
        cidr_bits = '1' * cidr_mask + '0' * (32 - cidr_mask)
        cidr_bits_arr = [str(int(cidr_bits[:8], 2)), str(int(cidr_bits[8:16], 2)), str(int(cidr_bits[16:24], 2)),
                         str(int(cidr_bits[24:], 2))]
        return '.'.join(cidr_bits_arr)

    @staticmethod
    def within(network1, network2):
        """
        Check whether or not one of the two given PyNetAddr objects are within the range of the other.
        :param network1: PyNetAddr object to check against param network2
        :param network2: PyNetAddr object to check against param network1
        :return: True of one of the objects is within the range of the other, False otherwise
        """
        if not isinstance(network1, PyNetAddr) or \
                not isinstance(network2, PyNetAddr):
            return False
        if network1.network == network2.network:
            return True
        mask1_splitter = network1.mask.split('.')
        mask2_splitter = network2.mask.split('.')
        total1 = int(mask1_splitter[0]) + int(mask1_splitter[1]) + int(mask1_splitter[2]) + int(mask1_splitter[3])
        total2 = int(mask2_splitter[0]) + int(mask2_splitter[1]) + int(mask2_splitter[2]) + int(mask2_splitter[3])
        if total1 < total2:
            netaddr3 = PyNetAddr(network2.network, network1.mask)
            if network1.network == netaddr3.network:
                return True
        elif total2 < total1:
            netaddr3 = PyNetAddr(network1.network, network2.mask)
            if network2.network == netaddr3.network:
                return True
        return False

    @staticmethod
    def summarize(subnets):
        """
        Compress a given list of subnets by removing those which are contained inside of others in the list
        :param subnets: list of PyNetAddr objects to summarize
        :return: sorted list of summarized PyNetAddr objects
        """
        # make sure we've actually received a list of PyNetAddr objects
        subnets = [sn for sn in subnets if isinstance(sn, PyNetAddr)]
        if len(subnets) == 0:
            return False
        sorted_nets = sorted(subnets, key=lambda sn: sn.cidr_mask)
        summarized = set()
        while len(sorted_nets) > 0:
            tmp_net = sorted_nets.pop()
            found = False
            for sn in sorted_nets:
                if PyNetAddr.within(tmp_net, sn):
                    summarized.add(sn)
                    found = True
                    break
            if not found:
                summarized.add(tmp_net)
        return sorted(summarized, key=lambda sn: "%s/%s" % (sn.cidr_mask, sn.network))

    def set_new(self, address, mask):
        """
        Set this object to a new address and mask.
        :param address: single IP address, or address and mask in CIDR notation (i.e. 10.0.0.0/24)
        :param mask: subnet mask in full notation (i.e. 255.255.255.0); None if address param is in CIDR notation
        :return: True if successful, False otherwise
        """
        if PyNetAddr.is_valid_addr(address.split("/")[0]):
            self.address = address.split("/")[0]
        else:
            print("Error, invalid IP address!")
            return False
        if mask is None:
            mask = PyNetAddr.calc_full_mask(int(address.split("/")[1]))
        if PyNetAddr.is_valid_mask(mask):
            self.mask = mask
            self.cidr_mask = PyNetAddr.calc_cidr_mask(self.mask)
        else:
            print("Error, invalid subnet mask!")
            return False
        self.network = PyNetAddr.calc_network(self.address, self.mask)
        self.broadcast = PyNetAddr.calc_broadcast(self.address, self.mask)
        self.range = PyNetAddr.calc_range(self.network, self.broadcast)
        return True
