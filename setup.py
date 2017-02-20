'''
Created on Jul 25, 2016

@author: t_songr
'''
from setuptools import setup

setup(name='gbXMLParser',
      version='0.69',
      description='Parser for gbXML file',
      url='https://git.autodesk.com/t-songr/gbXML_parser',
      author='Runsheng Song',
      author_email='runsheng@umail.ucsb.edu',
      license='MIT',
      packages = ['gbXMLParser'],    
#       package_data = {'gbXMLParser.ThorV2ConsoleBin/bin/Release':['*']},
      include_package_data=True,
      zip_safe=False)