# -*- coding: utf-8 -*-
from __future__ import with_statement
try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages
import cms_quickstart

with open('README.rst', 'r') as fobj:
    long_desc = fobj.read()
    
setup(
    name='django-cms-quickstart',
    version=cms_quickstart.__version__,
    url='https://github.com/ojii/django-cms-quickstart/',
    download_url='http://pypi.python.org/pypi/django-cms-quickstart',
    license='BSD',
    author='Jonas Obrist',
    author_email='jonas.obrist@divio.ch',
    description='Quickstart command line app for the django CMS',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    package_data={
        'cms_quickstart': [
            'template/*.cfg',
            'template/py_src/project/*.py',
            'template/py_src/project/settings/*.py',
            'template/py_src/project/templates/*.html',
            'template/py_src/project/media/css/*.css',
            'template/py_src/project/templates/js/libs/*.js',
        ],
    },
    entry_points={
        'console_scripts': [
            'cms-quickstart = cms_quickstart.quickstart:main',
        ],
    },
    install_requires=[
        "Django>=1.2",
    ],
)