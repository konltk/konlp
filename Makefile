# later on we would write this
# Copyright (C) 2017 - 0000 KoNLTK project
#
# Korean Natural Language Toolkit: source Makefile
#
# Author: HyunYoung Lee <hyun02.engineer@gmail.com>
#         GyuHyeon Nam <ngh3053@gmail.com>
#         Seungshik Kang <sskang@kookmin.ac.kr>
# URL: <https://www.konltk.org>
# For license information, see LICENSE.TXT
# ========================================================

# Deployment instructions
# 0. Fill in `pypirc.sample`, and `cp pypirc.sample ~/.pypirc`
#
#
# 1. $ make testpypi
# 2. $ make pypi # notice that you don't change the version number. 
# 3. Push tag 
# 4. updat the document 
 
PYTHON = python
PIP = pip
PACKAGE = konlp

# Before use testpypi and pypi, update pypirc.sample to $HOME/USERNAME/.pypir
# Then check the version 
# 
#   twine 1.8.0
#   setuptools 27.0.0
#   Python 2.7.13 (distutils update)
#   Python 3.4.6 (distutils update)
#   Python 3.5.3 (distutils update)
#   Python 3.6.0 (distutils update)
#
# https://packaging.python.org/guides/migrating-to-pypi-org/
# If you want to distribute sorce 
# --format option you can also one of zip and gztar.
# If you want to use zip, --format=zip OR if gztar, --format=gztar


##################################################################
#                                                                #
#                            testpypi                            #
#                                                                #
##################################################################

testpypi:
	$(PYTHON) setup.py register -r testpypi
	#$(PYTHON) setup.py sdist --format=gztar upload -r testpypi
	$(PYTHON) setup.py bdist_wheel upload -r testpypi
	# Execute manually below 
	# If you don't have the virtualenv, pip install virtualenv
	# cd /tmp
	# virtualenv venv
	# source venv/bin/activate
	# pip install --index-url https://test.pypi.org/simple/ konlp
	# deactivate 
	# virtualenv-3.5 venv3
	# source venv3/bin/activate
	# pip3 install --index-url https://test.pypi.org/simple/ konlp


##################################################################
#                                                                #
#                              pypi                              #
#                                                                #
##################################################################


pypi:
	$(PYTHON) setup.py register -r pypi
	#$(PYTHON) setup.py sdist --format=gztar upload -r pypi
	$(PYTHON) setup.py bdist_wheel upload -r pypi

clean:
	rm -rf build
	rm -rf dist
	rm -rf konlp.egg-info/

#clean_code:
#	rm -f `find konlp -name '*.pyc'`
#	rm -f `find konlp -name '*.pyo'`
