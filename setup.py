import os

import setuptools

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as f:
    desc = f.read()

about = {}  # type: ignore
with open(os.path.join(here, "remo", "__version__.py"), "r") as f:
    exec(f.read(), about)

setuptools.setup(
    name=about["__name__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=about["__license__"],
    description=about["__description__"],
    long_description=desc,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    keywords=["Nature Remo"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Topic :: Home Automation",
        "Topic :: Internet",
    ],
    packages=setuptools.find_packages(exclude="tests"),
    install_requires=[
        "marshmallow==3.7.1",
        "requests==2.24.0",
        "click==7.1.2",
    ],
    entry_points={"console_scripts": ["remo = remo.cli:main"]},
)
