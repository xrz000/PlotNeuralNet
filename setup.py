import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="plotnn",
    version="0.0.1",
    description="Plot neural networks by latex",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xrz000/PlotNeuralNet",
    packages=['plotnn'],
    package_data={'plotnn': ['layers/*', 'templates/*']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
