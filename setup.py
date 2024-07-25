from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='hello_world',
    version=version,
    description='test',
    author='bprashanth',
    author_email='prashanthseven@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
