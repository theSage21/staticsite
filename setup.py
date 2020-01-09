from setuptools import setup

__version__ = "2020.1.10"

with open("README.md", "r") as fl:
    long_desc = fl.read()


setup(
    name="staticsite",
    author="Arjoonn Sharma",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    version=__version__,
    packages=["staticsite"],
    install_requires=["jinja2", "htmlmin"],
    python_requires=">=3.6",
    project_urls={
        "Source": "https://github.com/thesage21/staticsite",
        "Documentation": "https://thesage21.github.io/staticsite/",
    },
    zip_safe=True,
)
