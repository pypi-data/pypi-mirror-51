from distutils.core import setup
import setuptools
from setuptools import find_packages

setup(
  name = "Logen",
  packages = find_packages(),                   # finds all packages and subpackages automatically
  entry_points = {
      "console_scripts": ["logen = Logen.main:main"]
  },
  version = "1.0.1",
  license = "MIT",
  description = "Generates and converts between various localization formats.",
  long_description = "Logen generates and converts between various localization formats so you don't need to remember how to do that!",
  author = "David Piper",
  author_email = "david@dpiper.de",
  url = "https://github.com/DavidPiper94",     # Provide either the link to your github or to your website
  download_url = "https://github.com/DavidPiper94/Logen/archive/v_1.0.1.tar.gz",
  keywords = [
      "localization",
      "converter",
      "ios",
      "android",
    ],
  classifiers = [
    "Development Status :: 4 - Beta",          # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    "Intended Audience :: Developers",          # Define that your audience are developers
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",      # Specify which pyhton versions that you want to support
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
  ],
)