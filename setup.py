from __future__ import print_function
from setuptools import setup, find_packages

setup(
    name="KubeGrade",
    version="0.0.2",
    author="KubeOperator",
    author_email="support@fit2cloud.com",
    description="A python library for scoring kubernetes",
    license="MIT License",
    url="https://github.com/KubeOperator/KubeGrade",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        "kubernetes>=10.0.1"
    ],
    zip_safe=True,
)
