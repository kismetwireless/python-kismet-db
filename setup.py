import os
import re
from setuptools import setup


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as f:
        filestring = f.read()
    return filestring


def get_version():
    raw_init_file = read("kismetdb/__init__.py")
    rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
    ver = rx_compiled.search(raw_init_file).group(1)
    return ver


def get_author():
    raw_init_file = read("kismetdb/__init__.py")
    rx_compiled = re.compile(r"\s*__author__\s*=\s*\"(.*)\"")
    author = rx_compiled.search(raw_init_file).group(1)
    return author


def get_copyright():
    raw_init_file = read("kismetdb/__init__.py")
    rx_compiled = re.compile(r"\s*__copyright__\s*=\s*\"(.*)\"")
    cright = rx_compiled.search(raw_init_file).group(1)
    return cright


def get_license():
    raw_init_file = read("kismetdb/__init__.py")
    rx_compiled = re.compile(r"\s*__license__\s*=\s*\"(.*)\"")
    ver = rx_compiled.search(raw_init_file).group(1)
    return ver


def get_email():
    raw_init_file = read("kismetdb/__init__.py")
    rx_compiled = re.compile(r"\s*__email__\s*=\s*\"(\S+)\"")
    email = rx_compiled.search(raw_init_file).group(1)
    return email


def build_long_desc():
    return "\n".join([read(f) for f in ["README.rst", "CHANGELOG.rst"]])


setup(name="kismetdb",
      version=get_version(),
      author=get_author(),
      author_email=get_email(),
      description="A python wrapper for the Kismet database",
      long_description=build_long_desc(),
      long_description_content_type="text/x-rst",
      license=get_license(),
      keywords="kismet",
      url="https://github.com/kismetwireless/python-kismet-db",
      packages=["kismetdb", "kismetdb.scripts"],
      install_requires=["python-dateutil", "simplekml"],
      entry_points={
          "console_scripts": [
              "kismet_log_devices_to_json = kismetdb.scripts.log_devices_to_json:main",  # NOQA
              "kismet_log_to_csv = kismetdb.scripts.log_to_csv:main",
              "kismet_log_to_kml = kismetdb.scripts.log_to_kml:main",
              "kismet_log_to_pcap = kismetdb.scripts.log_to_pcap:main",
              "kismet_log_devices_to_filebeat_json = kismetdb.scripts.log_devices_to_filebeat_json:main"]},  # NOQA
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Topic :: Security",
          "License :: OSI Approved :: BSD License"
          ],)
