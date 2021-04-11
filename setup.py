
from setuptools import find_packages, setup


setup(
    name="arls",
    version="1.0.1",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["arls=arls:main"],
    },
    include_package_data=True,
    package_data={
        '': ["*.npy"]
    }
)
