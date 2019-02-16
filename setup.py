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


def build_long_desc():
    return "\n".join([read(f) for f in ["README.rst", "CHANGELOG.rst"]])


setup(name="kismetdb",
      version=get_version(),
      author="Ash Wilson",
      author_email="ash.d.wilson@gmail.com",
      description="A python wrapper for the Kismet database",
      license="BSD",
      keywords="kismet",
      url="https://github.com/ashmastaflash/kismet-db",
      packages=["kismetdb", "kismetdb.scripts"],
      install_requires=["python-dateutil", "simplekml"],
      long_description=build_long_desc(),
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
