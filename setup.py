#!/usr/bin/env python3
"""
Setup script for Bruite Force Educational Web Security Testing Tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bruite-force",
    version="2.0.0",
    author="Educational Demo",
    author_email="demo@example.com",
    description="Educational Web Brute Force Tool for authorized security testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/bruite-force",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Security",
        "Topic :: Education",
        "License :: Educational Use Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "bruite-force=bruite_force.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "bruite_force": [
            "config.json",
            "wordlists/*.txt",
        ],
    },
    zip_safe=False,
    keywords="security testing education brute force web",
)
