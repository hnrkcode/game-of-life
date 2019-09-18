import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gameoflife",
    author="Henrik Petersson",
    author_email="henrik@tutamail.com",
    description="Python implementation of Conway's game of life algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.7.4",
    entry_points={"console_scripts": ["gameoflife = gameoflife.__main__:main"]},
)
