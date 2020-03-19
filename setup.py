from __future__ import print_function
from setuptools import setup, find_packages

setup(
    name="KubeGrade",
    version="0.0.1",
    author="KubeOperator",
    author_email="support@fit2cloud.com",
    description="A python library for scoring kubernetes",
    license="Apache License 2.0",
    url="https://github.com/KubeOperator/KubeGrade",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License 2.0',
        'Natural Language :: Chinese',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: NLP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        "kubernetes>=10.0.1"
    ],
    zip_safe=True,
)
