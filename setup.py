"""Setupup.py for data-structures repo."""

from setuptools import setup

setup(
    name="http-server",
    description="Implementation of an echo server using Python sockets.",
    version=0.1,
    author="Marc Fieser and Conor Clary",
    author_email="midfies@gmail.com",
    license="MIT",
    package_dir={'': 'src'},
    py_modules=['http-server'],
    install_requires=['ipython'],
    extras_require={
        "test": ['tox', 'pytest', 'pytest-watch', 'pytest-cov']
    },
)
