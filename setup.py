from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='helper',

    version='0.1.0',

    description='HELPeR is a private IFTTT',
    long_description=long_description,

    url='https://github.com/dschep/HELPeR',

    author='Daniel Schep',
    author_email='dschep@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4',
    ],

    keywords='django development',

    packages=find_packages(),

    install_requires=['django', 'requests', 'celery', 'django-stronghold',
                      'django-tastypie', 'psycopg2'],
)
