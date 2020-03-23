import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='solrcli',
     version='0.1.12',
     author="Andrea Carmisciano",
     author_email="andrea.carmisciano@gmail.com",
     description="A super simple Solr Cli",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/acarmisc/solrcli",
     packages=setuptools.find_packages(),
     scripts=['bin/solrcli'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[
            'certifi==2019.3.9',
            'chardet==3.0.4',
            'Click==7.0',
            'idna==2.8',
            'PyMySQL==0.9.3',
            'pysolr==3.8.1',
            'PyYAML==5.1.2',
            'requests==2.22.0',
            'tqdm==4.35.0',
            'urllib3==1.25.3',
            'xmltodict==0.12.0'
     ]
 )
