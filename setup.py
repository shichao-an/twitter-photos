from setuptools import setup, find_packages
from twphotos import __version__


setup(
    name='twitter-photos',
    version=__version__,
    description="Command-line tool to get photos from Twitter accounts.",
    long_description=open('README.rst').read(),
    keywords='twitter photos',
    author='Shichao An',
    author_email='shichao.an@nyu.edu',
    url='https://github.com/shichao-an/twitter-photos',
    license='BSD',
    install_requires=['python-twitter', 'requests', 'urllib3'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'twphotos = twphotos.photos:main',
        ],
    },
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
    ],
)
