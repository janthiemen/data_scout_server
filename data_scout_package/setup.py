from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Data Scout',
    version='0.1',
    description='This package provides the processing and transformation steps for Data Scout pipelines.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jan Thiemen Postema',
    author_email='info@scoutline.org',
    packages=find_packages(),
    url="https://github.com/janthiemen/data_scout/",
    project_urls={
        "Bug Tracker": "https://github.com/janthiemen/data_scout/issues",
        "Documentation": 'https://github.com/janthiemen/data_scout/',
        "Source Code": "https://github.com/janthiemen/data_scout/",
    },
    keywords = ['data', 'data preperation'],
    package_data={},
    include_package_data=True,
    install_requires=['pandas', 'xlrd'],
    python_requires='>=3.6',
    extras_require={
        'dev': [
            'nose2',
        ]
    },
    classifiers=[],
    test_suite='nose2.collector.collector',
)