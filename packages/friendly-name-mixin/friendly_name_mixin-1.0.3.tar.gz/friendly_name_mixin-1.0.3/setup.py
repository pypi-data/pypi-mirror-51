import sys
from setuptools import setup


if sys.version_info < (2, 6):
    print 'ERROR: friendly_name_mixin requires at least Python 2.6 to run.'
    sys.exit(1)


setup(
    name='friendly_name_mixin',
    version='1.0.3',
    url='https://github.com/petarmaric/friendly_name_mixin',
    license='BSD',
    author='Petar Maric',
    author_email='petarmaric@uns.ac.rs',
    description='Mixin class for extracting friendly names from classes',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    platforms='any',
    py_modules=['friendly_name_mixin'],
    setup_requires = ['nose>=1.0'],
    tests_require = ['coverage>=3.3', 'nose>=1.0', 'nosexcover>=1.0.7'],
    test_suite = 'nose.collector',
)
