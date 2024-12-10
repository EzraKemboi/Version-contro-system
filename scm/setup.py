from setuptools import setup, find_packages

setup(
    name="myscm",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "myscm=myscm.cli:main",
        ],
    },
    install_requires=[
        "colorama",
    ],
)
