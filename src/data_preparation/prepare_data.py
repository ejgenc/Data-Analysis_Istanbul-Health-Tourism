# -*- coding: utf-8 -*-

import os

for file in os.listdir():
	file_prefix = file.split(".")[1]
	if file_prefix == "py" and file != "prepare_data.py":
		print(file)