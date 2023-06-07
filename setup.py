from setuptools import setup, find_packages

setup(
    name='mvd',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'rich-click>=1.6.1',
    ],
    entry_points={
        'console_scripts': [
            'mvd = mvd.main:cli',
        ],
    },
)