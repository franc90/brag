from setuptools import setup, find_packages

setup(
    name='brag',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'pyfzf'
    ],
    entry_points={
        'console_scripts': [
            'brag=brag.app:main',
        ],
    },
)
