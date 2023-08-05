from distutils.core import setup

from setuptools import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='coolours',
    packages=['coolours'],
    version='0.5',
    license='MIT',
    description='A Python module to make text styling easy.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alex Hawking',
    author_email='alexrhawking@gmail.com',
    url='https://alexhawking.now.sh/',
    download_url='https://github.com/Handmade-Studios/coolors-module/archive/master.zip',
    keywords=['colour', 'easy', 'output',
              'terminal', 'colouring', 'color', 'cool', 'style', 'bold', 'underline'],
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
