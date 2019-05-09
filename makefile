#!/usr/bin/env python

all:
	@python3 pip/get-pip.py --user > /dev/null
	@python3 -m pip install numpy --user > /dev/null
	@chmod a+x simulator
