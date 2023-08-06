from setuptools import setup

import cognite_uploader

setup(
    # Application name:
    name="cognite-uploader",
    # Version number (initial):
    version=cognite_uploader.__version__,
    # Application author details:
    author="Mathias Lohne",
    author_email="mathias.lohne@cognite.com",
    # Include additional files into the package
    include_package_data=True,
    # Details
    url="https://github.com/cognitedata/python-uploader",
    packages=["cognite_uploader"],
    description="Uploader used in extractors.",
    # Dependent packages (distributions)
    install_requires=["cognite-sdk==1.1.*", "typing", "google-cloud-pubsub==0.41.*"],
)
