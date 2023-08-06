import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gaiaclient",
    version="0.0.16",
    license='MIT License',
    author="JOT Automation Ltd.",
    author_email="rami.rahikkala@jotautomation.com",
    description="Client for JOT Automation gaia machines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jotautomation/gaiapythonclient",
    py_modules=['gaiaclient'],
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
