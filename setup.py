from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-authdataset',
    version=version,
    description="Autirizacion para colocar un dataset visible",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Rodrigo Valdez',
    author_email='rodri.valdez@gmail.com',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.authdataset'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        # myplugin=ckanext.authdataset.plugin:PluginClass
	   auth_plugin=ckanext.authdataset.dataset:PruebaDatasetFormPlugin	
    ''',
)
