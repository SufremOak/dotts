from setuptools import setup, find_packages

setup(
    name='dotts',
    version='1.0.0',
    description='The Dotfiles Manager from the Future',
    author='SufremOak',
    author_email='migsufrem@gmail.com',
    url='https://github.com/yourusername/dotts',
    packages=find_packages(),
    install_requires=[
        'typer',
        'rich',
        'python-json-logger',
    ],
    entry_points={
        'console_scripts': [
            'dotts=main:app',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
