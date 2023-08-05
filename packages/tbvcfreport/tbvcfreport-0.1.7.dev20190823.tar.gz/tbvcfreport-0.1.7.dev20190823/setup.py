from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tbvcfreport',
    version='0.1.7',
    url='https://github.com/COMBAT-TB/tbvcfreport',
    author='SANBI',
    author_email='help@sanbi.ac.za',
    description="Parses SnpEff generated VCF and generates an HTML report.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='neo4j,vcf,tuberculosis,h37rv,snpeff',
    license="GPLv3",
    py_modules=['tbvcfreport'],
    packages=find_packages(),
    package_data={
        'tbvcfreport': ['templates/*.html'],
    },
    python_requires='~=3.6',
    install_requires=[
        'click',
        'py2neo',
        'jinja2',
        'tqdm',
        'pyvcf',
        'snpit',
    ],
    dependency_links=[
        'git+https://github.com/samlipworth/snpit.git@c531cb1eec640dfb5e66b6940a95284e5b900936#egg=snpit',
    ],
    entry_points={
        'console_scripts': ['tbvcfreport=tbvcfreport.tbvcfreport:cli']
    },
    project_urls={
        'Project': 'https://combattb.org',
        'Source': 'https://github.com/COMBAT-TB/tbvcfreport',
        'Tracker': 'https://github.com/COMBAT-TB/tbvcfreport/issues',
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
