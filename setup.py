import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_access_logs',
    version='0.1',
    packages=['access_logs'],
    include_package_data=True,
    license='Apache License, Version 2.0', 
    description='A simple module to record server access logs in DB and export them',
    long_description=README,
    url='https://github.com/TriplePoint-Software/django_access_logs',
    author='Jai',
    author_email='jaivikram.verma@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2.0 License', 
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires = [
        'django-constance>=0.6', 
        'ua-parser>=0.3.6', 
        'django-import-export>=0.2.7', 
        'python-dateutil>=2.4.2',
        'celery>=3.1.18', 
        'django-celery>=3.1.16', 
        ],
)
