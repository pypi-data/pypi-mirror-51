from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="itu_r_468_weighting",
    version="1.0.2",
    description="A zero dependency Python ITU-R 468 noise weighting filter (1 and 2 kHz)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cinelexi/itu_r_468_weighting",
    author="Alexis Michaltsis",
    author_email="a.michaltsis@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="ITU-R BS.468-4 SMPTE RP 2054:2010 noise weighting filter",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.6",
)
