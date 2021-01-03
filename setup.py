import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SerialManager-MSUSeconRobotics", # Replace with your own username
    version="0.1",
    author="Spencer Barnes",
    author_email="SWilliamBarnes@google.com",
    description="Package for multiprocess USB to Arduino comm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MSUSeconRobotics/SerialManager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)