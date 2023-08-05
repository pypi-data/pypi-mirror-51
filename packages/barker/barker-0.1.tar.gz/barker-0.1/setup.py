from setuptools import setup
import barker

classifiers = [
  "Programming Language :: Python :: 3",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: MIT License",
  "Topic :: Software Development :: Libraries",
  "Topic :: Utilities"
]

setup(name="barker",
      version=barker.__version__,
      author="Ethan Nelson",
      author_email="git@ethan-nelson.com",
      url="https://github.com/ethan-nelson/barker",
      py_modules=["barker"],
      description="Webhook class implementation",
      license="MIT"
      )
