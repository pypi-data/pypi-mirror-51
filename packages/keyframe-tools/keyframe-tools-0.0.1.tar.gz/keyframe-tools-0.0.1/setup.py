import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="keyframe-tools",
    version="0.0.1",
    author="Audrow Nash",
    author_email="audrowna@usc.edu",
    description="Generate movement from keyframes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/audrow/keyframe-tools",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
