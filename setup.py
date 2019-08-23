import setuptools

with open("README.md", "r") as fh:
    __long_description__ = fh.read()

setuptools.setup(
    name="lsan_tools",
    version="0.0.1",
    author="Shawn Rhoads",
    author_email="sr1209@sr1209@georgetown.edu",
    install_requires = "pandas>=0.24",
    description="Python toolbox with general-purpose functions for behavioral and neuroimaging research",
    long_description=__long_description__,
    url="https://github.com/LabSocialAffectNeuro/lsan_tools",
    packages=setuptools.find_packages(exclude=['']),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)