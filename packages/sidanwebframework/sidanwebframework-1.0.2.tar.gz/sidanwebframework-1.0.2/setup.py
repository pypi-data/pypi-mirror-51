import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sidanwebframework",
    version="1.0.2",
    author="sidan",
    description="sidanwebframework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/muhammedsidan/sidanwebframework/",
    packages=['sidanwebframework'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
