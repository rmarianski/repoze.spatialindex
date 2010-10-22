from setuptools import setup, find_packages
import sys, os

version = '0.1'

requires = [
    'zope.interface',
    'Rtree',
    'repoze.catalog',
    ]

setup(name='repoze.spatialindex',
      version=version,
      description="repoze.catalog rtree spatial index",
      long_description="""\
repoze.catalog rtree spatial index""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Robert Marianski',
      author_email='rob@marianski.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      namespace_packages=['repoze'],
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite='repoze.spatialindex',
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
