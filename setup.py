import os

from setuptools import setup, find_packages


def read_requirements(filename):
    """Open a requirements file and return list of its lines."""
    contents = read_file(filename).strip('\n')
    return contents.split('\n') if contents else []


def read_file(filename):
    """Open and a file, read it and return its contents."""
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path) as f:
        return f.read()


install_requires = read_requirements('requirements.txt')
tests_require = read_requirements('requirements_dev.txt')

setup(
    name='falcon-telegraf-middleware',
    version='2018.3.29.1',
    author='Webinterpret',
    author_email='funky_chicken@webinterpret.com',
    description='Falcon to Telegraf middlewares',
    long_description=read_file('README.md'),
    url='https://gitlab.devwebinterpret.com/kamil.e/falcon-telegraf-middleware',
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
)