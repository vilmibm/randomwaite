#!/usr/bin/env python

from setuptools import setup

setup(
    name='randomwaite',
    version='1.0.0',
    description='random tarot generator',
    url='https://github.com/nathanielksmith/randomwaite',
    author='vilmibm shaksfrpease',
    author_email='nks@lambdaphil.es',
    license='GPL',
    classifiers=[
        'Topic :: Artistic Software',
        'License :: OSI Approved :: GNU Affero General Public License v3 (AGPLv3)',
    ],
    keywords='tarot',
    packages=['randomwaite'],
    install_requires = ['flickrapi==2.1.2',
                        'Pillow==3.3.1',
                        'tweepy==3.5.0',
                        'pixelsorter==1.2',
                        'celery==3.1.23',
                        'redis==2.10.5',
    ],
    include_package_data = True,
    entry_points = {
          'console_scripts': [
              'randomwaite = randomwaite.__init__:main'
          ]
    },
)
