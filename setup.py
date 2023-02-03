import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# taken from https://github.com/CEA-COSMIC/ModOpt/blob/master/setup.py
with open('requirements.txt') as open_file:
    install_requires = open_file.read()

setuptools.setup(
    name="deq-flow",
    version="0.0.1",
    author="Shaojie Bai",
    author_email="shaojieb@cs.cmu.edu",
    description="DEQ Flow.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/locuslab/deq-flow",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    python_requires='>=3.6',
)
