import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

DEPENDENCIES = ['nose==1.3.7']

setuptools.setup(
    name="c-log-parser",
    version="0.0.1",
    author="Estefania Otero Garcia",
    author_email="estefania.otero.garcia@gmail.com",
    description="A simple package for log parsing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eoterogarcia/c-log-parser",
    install_requires=DEPENDENCIES,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='==3.8',
)