from pathlib import Path
from setuptools import setup, find_packages

PACKAGE_NAME = "core"
PACKAGE_VERSION = "0.1.0"
AUTHOR = "Ezequiel Leonardo Castaño"
AUTHOR_EMAIL = "-"
DESCRIPTION = "Course material to use along with the classes"
URL = "https://github.com/ELC/sistemas-de-gestion"
LICENSE = "MIT"
PACKAGE_DIR = "."
LONG_DESCRIPTION = Path("README.md").read_text(encoding="utf-8")

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    license=LICENSE,
    packages=find_packages(where=PACKAGE_DIR),
    package_dir={"": PACKAGE_DIR},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    setup_requires='setuptools-pipfile',
    use_pipfile=True,
)