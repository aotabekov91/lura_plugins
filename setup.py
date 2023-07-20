from setuptools import setup

setup(name='lura', 
      version='0.0.1', 
      description='Lura',
      entry_points = {
          'console_scripts': [
              'lura = lura.run:main',
              ],              
          },
      )
