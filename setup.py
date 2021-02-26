"""Create, read, modify, and write SunVox files."""

import io
import os
import re

from setuptools import find_packages, setup

# import sys
# from pathlib import Path


# SETUP_PATH = Path(__file__).parent.absolute()
# SRC_PYTHON_PATH = SETUP_PATH / "src" / "python"
# sys.path.append(SRC_PYTHON_PATH)
## import genrv  # NOQA isort:skip

dependencies = [
    "attrs >= 19.3.0",
    "awesome-slugify",
    "hexdump",
    "logutils",
    "networkx",
    "pyyaml",
]


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ).read()


badges_re = re.compile(r"^\.\.\s+start-badges.*^\.\.\s+end-badges", re.M | re.S)
uml_re = re.compile(r"^\.\.\s+uml::.*^\s+@enduml", re.M | re.S)

readme = read("README.rst")
readme = badges_re.sub("", readme)
readme = uml_re.sub("", readme)

changelog = re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst"))

long_description = "{}\n{}".format(readme, changelog)

setup(
    name="radiant-voices",
    version="1.0.0",  # [TODO] generate this using a tool
    url="https://github.com/metrasynth/radiant-voices",
    license="MIT",
    author="Matthew Scott",
    author_email="matt@11craft.com",
    description=__doc__,
    long_description=long_description,
    package_dir={"": "src/python"},
    packages=find_packages(where="src/python", include=["rv", "rv.*"]),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=dependencies,
    entry_points={},
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # "Development Status :: 2 - Pre-Alpha",
        # 'Development Status :: 3 - Alpha',
        "Development Status :: 4 - Beta",
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
