import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matrix_blockstack_password_provider",
    version="0.7.0",
    author="OpenIntents",
    author_email="support@openintents.org",
    description="Password provider for blockstack/EOS synapse server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/friedger/matrix_blockstack_password_provider",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "blockstack_zones-py3", "twisted"],
)
