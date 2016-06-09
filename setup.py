import os
from setuptools import setup

__version__ = "0.1.6"

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_access_logs',
    version=__version__,
    packages=['access_logs', 'access_logs.migrations'],
    include_package_data=True,
    license='Apache License, Version 2.0',
    description='A simple module to record server access logs in DB and export them',
    long_description="A simple reusable Django app to record parsed server access logs "
                     "in a database and export them as CSV on demand",
    url='https://github.com/TriplePoint-Software/django_access_logs',
    author='Jai',
    author_email='jaivikram.verma@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'celery>=3.1.18',
        'django-celery>=3.1.16',
        'django-import-export>=0.2.7',
        'django-solo>=1.1.2',
        'django>=1.7,<1.10',
        'python-dateutil>=2.4.2',
        'ua-parser>=0.3.6',
    ],
)
