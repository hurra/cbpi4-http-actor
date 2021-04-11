from setuptools import setup

setup(name='cbpi4-http-actor',
      version='0.0.1',
      description='CraftBeerPi Plugin',
      author='Lorenz Röhrl',
      author_email='sheepshit@gmx.de',
      url='https://github.com/hurra/cbpi4-http-actor',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-http-actor': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-http-actor'],
     )
