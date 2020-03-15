import sys
from os import path, listdir
from pathlib import Path
from typing import List, Tuple

from setuptools import find_packages
from sslyze import __author__, __email__, __version__, PROJECT_URL

# Setup file based on https://github.com/pypa/sampleproject/blob/master/setup.py
root_path = Path(__file__).parent.absolute()

# For cx_freeze builds, we need a special setup() function
if len(sys.argv) > 1 and sys.argv[1] == "build_exe":
    from cx_Freeze import setup
    from cx_Freeze import Executable
else:
    from setuptools import setup

    # Create fake Executable that does nothing so the setup.py file can be used on Linux
    class Executable:  # type: ignore
        def __init__(self, script, targetName):  # type: ignore
            pass


def get_long_description() -> str:
    path_to_readme = root_path / "README.md"
    return path_to_readme.read_text()


def get_include_files() -> List[Tuple[str, str]]:
    """"Get the list of trust stores so they properly packaged when doing a cx_freeze build.
    """
    plugin_data_files = []
    trust_stores_pem_path = root_path / "sslyze" / "plugins" / "certificate_info" / "trust_stores" / "pem_files"
    for file in listdir(trust_stores_pem_path):
        file = path.join(trust_stores_pem_path, file)
        if path.isfile(file):  # skip directories
            filename = path.basename(file)
            plugin_data_files.append((file, path.join("pem_files", filename)))
    return plugin_data_files


setup(
    name="sslyze",
    version=__version__,
    description="Fast and powerful SSL/TLS server scanning library",
    python_requires=">=3.6",
    # Pypi metadata
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url=PROJECT_URL,
    author=__author__,
    author_email=__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: French",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.6",
        "Topic :: System :: Networking",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Security",
    ],
    keywords="ssl tls scan security library",
    project_urls={
        "Source": "https://github.com/nabla-c0d3/sslyze",
        "Changelog": "https://github.com/nabla-c0d3/sslyze/releases",
        "Documentation": "https://nabla-c0d3.github.io/sslyze/documentation",
    },
    # Package info
    packages=find_packages(exclude=["docs", "tests"]),
    package_data={
        "sslyze": ["py.typed"],
        "sslyze.plugins.certificate_info.trust_stores": ["pem_files/*.pem", "pem_files/*.yaml"],
    },
    entry_points={"console_scripts": ["sslyze = sslyze.__main__:main"]},
    # Dependencies
    install_requires=[
        "nassl>=2.2.0,<2.3.0",
        "cryptography==2.5",
        "tls-parser>=1.2.0,<1.3.0",
        "dataclasses ; python_version<'3.7'",  # To remove when we drop support for Python 3.6
    ],
    # cx_freeze info for Windows builds with Python embedded
    options={"build_exe": {"packages": ["cffi", "cryptography", "idna"], "include_files": get_include_files()}},
    executables=[Executable(path.join("sslyze", "__main__.py"), targetName="sslyze.exe")],
)
