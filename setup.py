from setuptools import setup, find_packages
import os

version = '1.2.1'

entry_points = {
    'openprocurement.auctions.core.plugins': [
        'auctions.landlease.other = openprocurement.auctions.landlease.includeme:includeme_other',
        'auctions.landlease.financial = openprocurement.auctions.landlease.includeme:includeme_financial'
    ],
    'openprocurement.auctions.landlease.plugins': [
        'landlease.other.migration = openprocurement.auctions.landlease.migration:migrate_data',
        'landlease.financial.migration = openprocurement.auctions.landlease.migration:migrate_data'
    ]
}

requires = [
    'setuptools',
    'openprocurement.api',
    'openprocurement.auctions.core',
]

test_requires = requires + []

docs_requires = requires + [
    'sphinxcontrib-httpdomain',
]

setup(name='openprocurement.auctions.landlease',
      version=version,
      description="",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Quintagroup, Ltd.',
      author_email='info@quintagroup.com',
      license='Apache License 2.0',
      url='https://github.com/openprocurement/openprocurement.auctions.landlease',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['openprocurement', 'openprocurement.auctions'],
      include_package_data=True,
      zip_safe=False,
      extras_require={'docs': docs_requires, 'test': test_requires},
      install_requires=requires,
      entry_points=entry_points,
      )
