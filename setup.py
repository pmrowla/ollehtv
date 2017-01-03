from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    try:
        import pypandoc
        long_description = pypandoc.convert_text(
            long_description, 'rst', format='md')
    except ImportError:
        pass

setup(
    name='ollehtv',
    version='0.1.0',
    description='Python library for controlling an Olleh TV STB',
    long_description=long_description,
    url='https://github.com/pmrowla/ollehtv',
    author='Peter Rowlands',
    author_email='peter@pmrowla.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Multimedia',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='olleh ollehtv',
    py_modules=['ollehtv'],
    install_requires=['future', 'requests'],
)
