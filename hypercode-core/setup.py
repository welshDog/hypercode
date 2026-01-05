from setuptools import setup, find_packages

setup(
    name="hypercode",
    version="0.2.0-alpha",
    packages=find_packages(),
    install_requires=[
        # Core requirements
    ],
    extras_require={
        'qiskit': ['qiskit>=1.0.0', 'qiskit-aer>=0.13.0'],
    },
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'hypercode=hypercode.cli:main',
        ],
    },
)
