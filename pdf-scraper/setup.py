# coding=utf-8
from setuptools import setup, find_packages


with open('README.rst') as f:
    long_description = ''.join(f.readlines())

extras_require = {
    'docs': [
        'sphinx==1.8.5',
    ],
    'postgresql': [
        'asyncpg'
    ],
    'mysql': [
        'aiomysql'
    ],
}

setup(
    name='isir-explorer',
    version='0.1.0',
    description='Data extraction tool from Czech insolvency register (ISIR)',
    long_description=long_description,
    author='Pavel Tůma',
    author_email='tumapav3@fit.cvut.cz',
    keywords='isir,scraper',
    license='GPLv3+',
    url='https://github.com/opendatalabcz/isir-explorer',
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'betamax', 'flexmock'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
        'Topic :: Internet',
        'Topic :: Utilities',
        ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'isir-scraper = isir_explorer.scraper.main:main',
            'isir-dbimport = isir_explorer.dbimport.main:main',
            'isir-ws = isir_explorer.webservice.main:main',
            'isir-dl = isir_explorer.downloader.main:main',
            'isir-stats = isir_explorer.stats.main:main',
        ],
    },
    install_requires=[
        'configparser>=5',
        'click>=7',
        'regex>=2020.10.28',
        'databases>=0.4.1',
        'aiohttp>=3.6.2',
        'python-dateutil>=2.8.1',
        'aiofiles>=0.6.0',
    ],
    extras_require=extras_require,
)
