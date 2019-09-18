import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setuptools.setup(
     name='solrcli',  
     py_modules=['solrcli'],
     version='0.1.3',
     author="Andrea Carmisciano",
     author_email="andrea.carmisciano@gmail.com",
     description="A super simple Solr Cli",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/acarmisc/solrcli",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=requirements
 )
