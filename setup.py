from setuptools import setup, find_packages

version = '1.0.3'

entry_points = {
    'openprocurement.auctions.core.plugins': [
        'auctions.geb = openprocurement.auctions.geb.includeme:includeme',
    ],
    'openprocurement.auctions.geb.plugins': [
        'geb.migration = openprocurement.auctions.geb.migration:migrate_data',
    ]
}

test_requires = [
    'webtest',
    'python-coveralls',
    'mock',
    'munch',
    'freezegun'
]

setup(name='openprocurement.auctions.geb',
      version=version,
      description="",
      long_description=open("README.md").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Quintagroup, Ltd.',
      tests_require=test_requires,
      extras_require={'test': test_requires},
      author_email='info@quintagroup.com',
      license='Apache License 2.0',
      url='https://github.com/openprocurement/openprocurement.auctions.geb',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['openprocurement', 'openprocurement.auctions'],
      include_package_data=True,
      zip_safe=False,
      entry_points=entry_points,
      )
