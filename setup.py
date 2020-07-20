import setuptools

with open("README.md") as f:
    desc = f.read()

setuptools.setup(
    name="nature-remo",
    version="0.0.1",
    author="Shinya Fujino",
    author_email="shf0811@gmail.com",
    license="MIT",
    description="Python client for Nature Remo API",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/morinokami/nature-remo",
    keywords=["Nature Remo"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Home Automation",
        "Topic :: Internet",
    ],
    packages=setuptools.find_packages(exclude="tests"),
    install_requires=["requests"],
)
