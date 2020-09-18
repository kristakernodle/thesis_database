import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thesis-database-kristakernodle",
    version="0.0.1",
    author="Krista Kernodle",
    author_email="kkrista@umich.edu",
    description="Custom ORM for my thesis work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kristakernodle/thesis_database",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
