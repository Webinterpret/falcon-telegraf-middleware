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
    version='2021.06.01.1',
    author='Webinterpret',
    author_email='funky_chicken@webinterpret.com',
    description='Falcon to Telegraf middlewares',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/Webinterpret/falcon-telegraf-middleware',
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License'
    ],
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
)
