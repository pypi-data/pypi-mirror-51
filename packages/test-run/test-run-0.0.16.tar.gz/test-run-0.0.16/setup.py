from setuptools import setup
import setuptools
#from distutils.core import setup
def readme():
	with open('README.md') as f:
		README=f.read()
	return README

setup(
	name="test-run",
	version="0.0.16",
	description="A Python package to print",
	long_description=readme(),
	long_description_content_type=["text/markdown"],
	author="ANOOP SINGH RANA",
	author_email="apours986@gmail.com",
	license="MIT",
	classifiers=[
		"Programming Language :: Python :: 3",
	],
	#packages="test_run", thisw was for python3 but u need each nd every directory separately
	packages=["test_run"],
	include_package_data=True,
	entry_points={
		"console_scripts":  [
			"test-run=test_run._main:main",
		]
	},
)
