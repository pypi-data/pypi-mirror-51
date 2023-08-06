#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##

import os
import shutil
import errno
import fnmatch
import stat
# Local import
from . import debug
from . import env

"""
	
"""
def get_run_path():
	return os.getcwd()

"""
	
"""
def get_current_path(file):
	return os.path.dirname(os.path.realpath(file))

def create_directory_of_file(file):
	path = os.path.dirname(file)
	try:
		os.stat(path)
	except:
		os.makedirs(path)

def get_list_sub_path(path):
	# TODO : os.listdir(path)
	for dirname, dirnames, filenames in os.walk(path):
		return dirnames
	return []

def remove_path_and_sub_path(path):
	if os.path.isdir(path):
		debug.verbose("remove path : '" + path + "'")
		shutil.rmtree(path)

def remove_file(path):
	if os.path.isfile(path):
		os.remove(path)
	elif os.path.islink(path):
		os.remove(path)

def file_size(path):
	if not os.path.isfile(path):
		return 0
	statinfo = os.stat(path)
	return statinfo.st_size

def file_read_data(path, binary=False):
	if not os.path.isfile(path):
		return ""
	if binary == True:
		file = open(path, "rb")
	else:
		file = open(path, "r")
	data_file = file.read()
	file.close()
	return data_file

def version_to_string(version):
	version_ID = ""
	for id in version:
		if len(version_ID) != 0:
			if type(id) == str:
				version_ID += "-"
			else:
				version_ID += "."
		version_ID += str(id)
	return version_ID

##
## @brief Write data in a specific path.
## @param[in] path Path of the data might be written.
## @param[in] data Data To write in the file.
## @param[in] only_if_new (default: False) Write data only if data is different.
## @return True Something has been copied
## @return False Nothing has been copied
##
def file_write_data(path, data, only_if_new=False):
	if only_if_new == True:
		old_data = file_read_data(path)
		if old_data == data:
			return False
	#real write of data:
	create_directory_of_file(path)
	file = open(path, "w")
	file.write(data)
	file.close()
	return True

def list_to_str(list):
	if type(list) == type(str()):
		return list + " "
	else:
		result = ""
		# mulyiple imput in the list ...
		for elem in list:
			result += list_to_str(elem)
		return result

def add_prefix(prefix,list):
	if type(list) == type(None):
		return ""
	if type(list) == type(str()):
		return prefix+list
	else:
		if len(list)==0:
			return ''
		else:
			result=[]
			for elem in list:
				result.append(prefix+elem)
			return result

##
## @brief Clean a path from all un-needed element in a directory
## @param[in] path Path to clean
## @param[in] normal_list List of all files/path in the path
## @return True Something has been removed
## @return False Nothing has been removed
##
def clean_directory(path, normal_list):
	has_file_removed = False
	# get a list of all element in the path:
	for root, dirnames, filenames in os.walk(path):
		for file in filenames:
			file_name = os.path.join(root, file)
			if file_name not in normal_list:
				debug.print_element("remove file ", os.path.relpath(file_name), "==>", "---")
				os.remove(file_name)
				has_file_removed = True
	return has_file_removed

def filter_extention(list_files, extentions, invert=False):
	out = []
	for file in list_files:
		in_list = False
		for ext in extentions:
			if file[-len(ext):] == ext:
				in_list = True
		if     in_list == True \
		   and invert == False:
			out.append(file)
		elif     in_list == False \
		     and invert == True:
			out.append(file)
	return out


def move_if_needed(src, dst):
	if not os.path.isfile(src):
		debug.error("request move if needed, but file does not exist: '" + str(src) + "' to '" + str(dst) + "'")
		return
	src_data = file_read_data(src)
	if os.path.isfile(dst):
		# file exist ==> must check ...
		dst_data = file_read_data(dst)
		if src_data == dst_data:
			# nothing to do ...
			return
	file_write_data(dst, src_data)
	remove_file(src)

def store_command(cmd_line, file):
	# write cmd line only after to prevent errors ...
	if    file == "" \
	   or file == None:
		return;
	debug.verbose("create cmd file: " + file)
	# Create directory:
	create_directory_of_file(file)
	# Store the command Line:
	file2 = open(file, "w")
	file2.write(cmd_line)
	file2.flush()
	file2.close()

def store_warning(file, output, err):
	# write warning line only after to prevent errors ...
	if    file == "" \
	   or file == None:
		return;
	if env.get_warning_mode() == False:
		debug.verbose("remove warning file: " + file)
		# remove file if exist...
		remove_file(file);
		return;
	debug.verbose("create warning file: " + file)
	# Create directory:
	create_directory_of_file(file)
	# Store the command Line:
	file2 = open(file, "w")
	file2.write("===== output =====\n")
	file2.write(output)
	file2.write("\n\n")
	file2.write("===== error =====\n")
	file2.write(err)
	file2.write("\n\n")
	file2.flush()
	file2.close()


## List tools:
def list_append_and_check(listout, newElement, order):
	for element in listout:
		if element==newElement:
			return
	listout.append(newElement)
	if order == True:
		if type(newElement) is not dict:
			listout.sort()

def list_append_to(out_list, in_list, order=False):
	if type(in_list) == str:
		list_append_and_check(out_list, in_list, order)
	elif type(in_list) == list:
		# mulyiple imput in the list ...
		for elem in in_list:
			list_append_and_check(out_list, elem, order)
	elif type(in_list) == dict:
		list_append_and_check(out_list, in_list, order)
	else:
		debug.warning("can not add in list other than {list/dict/str} : " + str(type(in_list)))

def list_append_to_2(listout, module, list, order=False):
	# sepcial cse of bool
	if type(list) == bool:
		listout[module] = list
		return
	# add list in the Map
	if module not in listout:
		listout[module] = []
	# add elements...
	list_append_to(listout[module], list, order)



##
## @brief The vertion number can be set in an external file to permit to have a singe position to change when create a vew version
## @param[in] path_module (string) Path of the module position
## @param[in] filename_or_version (string or list) Path of the version or the real version lint parameter
## @return (list) List of version number
##
def get_version_from_file_or_direct(path_module, filename_or_version):
	# check case of iser set the version directly
	if type(filename_or_version) == list:
		return filename_or_version
	# this use a version file
	file_data = file_read_data(os.path.join(path_module, filename_or_version))
	if len(file_data) == 0:
		debug.warning("not enought data in the file version size=0 " + path_module + " / " + filename_or_version)
		return [0,0,0]
	lines = file_data.split("\n")
	if len(lines) != 1:
		debug.warning("More thatn one line in the file version ==> bas case use mode: 'XX', XX.YYY', 'XX.Y.ZZZ' or 'XX.Y-dev' : " + path_module + " / " + filename_or_version)
		return [0,0,0]
	line = lines[0]
	debug.debug("Parse line: '" + line + "'")
	#check if we have "-dev"
	dev_mode = False
	if line[-4:] == "-dev":
		dev_mode = True
		line = line[:-4]
	out = []
	list_elem = line.split('.')
	for elem in list_elem:
		out.append(int(elem))
	if dev_mode == True:
		out.append("dev")
	debug.debug("    ==> " + str(out))
	return out

##
## @brief Get the list of the authors frim an input list or a file
## @param[in] path_module (string) Path of the module position
## @param[in] filename_or_version (string or list) Path of the author file or the real list of authors
## @return (list) List of authors
##
def get_maintainer_from_file_or_direct(path_module, filename_or_author):
	# check case of iser set the version directly
	if type(filename_or_author) == list:
		return filename_or_author
	# this use a version file
	file_data = file_read_data(os.path.join(path_module, filename_or_author))
	if len(file_data) == 0:
		debug.warning("not enought data in the file author size=0 " + path_module + " / " + filename_or_author)
		return []
	# One user by line and # for comment line
	out = []
	for elem in file_data.split('\n'):
		if len(elem) == 0:
			continue
		if elem[0] == "#":
			# comment ...
			continue
		out.append(elem)
	return out

