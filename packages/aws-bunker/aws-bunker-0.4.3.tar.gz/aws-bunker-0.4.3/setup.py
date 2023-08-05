import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-bunker",
    version="0.4.3",
    author="Andy Klier, Gus Clemens",
    author_email="andyklier@gmail.com",
    description="bunker is a command line program for setting up an ec2 in AWS for remote development or as a backup. It can clone your git repos, and transfer ignored files from your machine to the ec2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/shindagger/bunker",
    packages=['bunker'],
    include_package_data=True,
    install_requires= ['setuptools', 'boto3', 'inquirer', 'paramiko', 'tqdm'],
    entry_points = {
        'console_scripts': ['bunker=bunker.bunker:bunker'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
