#!/usr/bin/env python

from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='investpy',
    version='0.8.8',
    packages=find_packages(),
    url='https://investpy.readthedocs.io/',
    download_url='https://github.com/alvarob96/investpy/archive/0.8.8.tar.gz',
    license='MIT License',
    author='Alvaro Bartolome',
    author_email='alvarob96@usal.es',
    description='investpy — a Python package for financial historical data extraction from Investing',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=['requests==2.22.0',
                      'pandas==0.24.2',
                      'Unidecode==1.0.23',
                      'lxml==4.3.3'],
    data_files=[
        ('equities', ['investpy/resources/equities/equities.csv']),
        ('funds', ['investpy/resources/funds/funds.csv']),
        ('etfs', ['investpy/resources/etfs/etfs.csv', 'investpy/resources/etfs/etf_markets.csv']),
        ('user_agents', ['investpy/resources/user_agent_list.txt'])
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries"
    ],
    keywords='investing, investing-api, spanish-stock-market, scraper, historical-data, financial-data, finance',
    python_requires='>=3',
    project_urls={
        'Bug Reports': 'https://github.com/alvarob96/investpy/issues',
        'Source': 'https://github.com/alvarob96/investpy',
        'Documentation': 'https://investpy.readthedocs.io/'
    },
)
