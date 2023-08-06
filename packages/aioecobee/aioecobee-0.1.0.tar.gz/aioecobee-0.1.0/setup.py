import setuptools

long_description = open('README.md').read()

setuptools.setup(
    name="aioecobee",
    version="0.1.0",
    author="Mark Coombes",
    author_email="mark@markcoombes.ca",
    description="Python3 async library for interacting with the ecobee API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marthoc/aioecobee",
    packages=['aioecobee'],
    install_requires=['aiofiles', 'aiohttp', 'asyncio'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
