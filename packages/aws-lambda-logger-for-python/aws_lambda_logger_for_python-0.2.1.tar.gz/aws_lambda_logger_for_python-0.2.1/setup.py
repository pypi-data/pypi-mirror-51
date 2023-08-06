from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

with open(path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(
    version=version,
    name='aws_lambda_logger_for_python',
    description='Nanolib to enhance logging in aws lambda',
    long_description=long_description,
    py_modules=['aws_lambda_logging'],
    url='https://github.com/Marcin-Duszynski/aws-lambda-logger-for-python',
    licence='MIT',
    extras_require={
        'tests': [
            'flake8-import-order',
            'pylama',
            'pytest',
            'pytest-cov',
            'pytest-runner',
            'tox',
        ],
        'dev': [
            'bumpversion',
            'twine',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)
