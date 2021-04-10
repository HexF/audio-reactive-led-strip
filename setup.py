
from setuptools import find_packages, setup


setup(
    name="arls",
    version="1.0.0",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["arls=arls:main"],
    },
)
