from setuptools import find_packages, setup

# The text of the README file
with open("README.md") as file:
    README = file.read()

# This call to setup() does all the work
setup(
    name="mcneelat-pyutils",
    version="1.9.0",
    description="A collection of helpful Python utilities to simplify dealing with databases, Kafka, and more.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tommym89/pyutils",
    author="Tommy McNeela",
    author_email="mcneelat@gmail.com",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["dnspython", "kafka-python", "psycopg2-binary", "python-ldap", "requests"],
)
