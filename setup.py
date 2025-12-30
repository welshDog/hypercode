from setuptools import setup, find_packages

setup(
    name="hypercode",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'antlr4-python3-runtime>=4.13.1',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'hypercode=hypercode.cli:main',
        ],
    },
)
