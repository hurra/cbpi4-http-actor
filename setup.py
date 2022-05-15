from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cbpi4-http-actor',
      version='0.0.4',
      description='Generic CraftBeerPi HTTP Actor Plugin',
      author='Lorenz Röhrl',
      author_email='sheepshit@gmx.de',
      url='https://github.com/hurra/cbpi4-http-actor',
      license='GPLv3',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-http-actor': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-http-actor'],
      install_requires=[
            'cbpi4>=4.0.0.34',
      ],
      long_description=long_description,
      long_description_content_type='text/markdown'
     )
