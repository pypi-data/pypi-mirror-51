import sys
from setuptools import setup, find_packages


CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
Maestral requires Python {}.{}, but you're trying to install it on
Python {}.{}. This may be because you are using a version of pip that
doesn't understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python3 -m pip install --upgrade pip setuptools
    $ python3 -m pip install maestral

""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


def get_version(relpath):
    """Read version info from a file without importing it"""
    from os.path import dirname, join

    if "__file__" not in globals():
        # Allow to use function interactively
        root = "."
    else:
        root = dirname(__file__)

    # The code below reads text file with unknown encoding in
    # in Python2/3 compatible way. Reading this text file
    # without specifying encoding will fail in Python 3 on some
    # systems (see http://goo.gl/5XmOH). Specifying encoding as
    # open() parameter is incompatible with Python 2

    # cp437 is the encoding without missing points, safe against:
    #   UnicodeDecodeError: 'charmap' codec can't decode byte...

    for line in open(join(root, relpath), "rb"):
        line = line.decode("cp437")
        if "__version__" in line:
            if '"' in line:
                return line.split('"')[1]
            elif "'" in line:
                return line.split("'")[1]


setup(
    name="maestral",
    version=get_version("maestral/main.py"),
    description="Open-source Dropbox client for macOS and Linux.",
    url="https://github.com/SamSchott/maestral",
    author="Sam Schott",
    author_email="ss2151@cam.ac.uk",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
            "maestral": [
                    "gui/resources/*.ui",
                    "gui/resources/*.icns",
                    "gui/resources/*.png",
                    "gui/resources/*.svg",
                    "gui/resources/icon-theme-gnome/*.theme",
                    "gui/resources/icon-theme-gnome/*/*/*.svg",
                    "bin/*.sh",
                    ],
            },
    install_requires=[
        "blinker",
        "click>=7.0",
        "dropbox>=9.4.0",
        "keyring>=19.0.0",
        "keyrings.alt>=3.0.0",
        "Pyro4",
        "requests",
        "u-msgpack-python",
        "watchdog",
    ],
    zip_safe=False,
    entry_points={
      "console_scripts": ["maestral=maestral.cli:main"],
    },
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
