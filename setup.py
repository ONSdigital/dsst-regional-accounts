from setuptools import setup, find_packages

setup(
    name='example_name',
    version='0.1.0-dev0',
    description='example_description',
    url='example_url',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(where="example_package"),
    # install_requires=,
    python_requires=">=3.6",
)
