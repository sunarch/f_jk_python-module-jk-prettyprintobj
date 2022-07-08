################################################################################
################################################################################
###
###  This file is automatically generated. Do not change this file! Changes
###  will get overwritten! Change the source file for "setup.py" instead.
###  This is either 'packageinfo.json' or 'packageinfo.jsonc'
###
################################################################################
################################################################################


from setuptools import setup

def readme():
	with open("README.md", "r", encoding="UTF-8-sig") as f:
		return f.read()

setup(
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python :: 3",
		"Topic :: Software Development :: Testing",
	],
	description = "This python module provides a mixin for creating pretty debugging output for objects. This is especially useful for semi-complex data structures.",
	include_package_data = False,
	install_requires = [
	],
	keywords = [
		"pretty-print",
		"debugging",
		"debug",
	],
	license = "Apache2",
	name = "jk_prettyprintobj",
	packages = [
		"jk_prettyprintobj",
	],
	version = "0.2022.1.18",
	zip_safe = False,
	long_description = readme(),
	long_description_content_type="text/markdown",
)
