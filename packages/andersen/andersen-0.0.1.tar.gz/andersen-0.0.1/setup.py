from __future__ import print_function
from setuptools import setup, find_packages
import os

README_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')

setup(
    name='andersen',
    version='0.0.1',
    description=(
        'python log library'
    ),
    long_description=open(README_FILE, encoding='utf8').read(),
    long_description_content_type="text/markdown",
    author='idlefish',
    author_email='lvhuanle12@126.com',
    maintainer='idlefish',
    maintainer_email='lvhuanle12@126.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://gitee.com/happy3014/andersen',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'toml'
    ]
)
