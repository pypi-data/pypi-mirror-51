# coding=utf-8
from setuptools import setup, find_packages
setup(
    name='qcloud-python-sts',
    version='3.0.3',
    description='this is sts for python on v3',
    url='https://github.com/tencentyun/qcloud-cos-sts-sdk',
    author='qcloudterminal',
    author_email='qcloudterminal@gmail.com',
    license='MIT',
    packages= find_packages(),
    install_requires=['requests']
)
