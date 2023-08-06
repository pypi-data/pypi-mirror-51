#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##

# Local import
from . import debug



force_mode=False

def set_force_mode(val):
	global force_mode
	if val==1:
		force_mode = 1
	else:
		force_mode = 0

def get_force_mode():
	global force_mode
	return force_mode

force_optimisation=False

def set_force_optimisation(val):
	global force_optimisation
	if val==1:
		force_optimisation = 1
	else:
		force_optimisation = 0

def get_force_optimisation():
	global force_optimisation
	return force_optimisation

parse_depth = 9999999

def set_parse_depth(val):
	global parse_depth
	parse_depth = val
	debug.debug("Set depth search element: " + str(parse_depth))

def get_parse_depth():
	global parse_depth
	return parse_depth

exclude_search_path = []

def set_exclude_search_path(val):
	global exclude_search_path
	exclude_search_path = val
	debug.debug("Set depth search element: " + str(exclude_search_path))

def get_exclude_search_path():
	global exclude_search_path
	return exclude_search_path


build_system_base_name = "doxy"

def set_build_system_base_name(val):
	global build_system_base_name
	build_system_base_name = val
	debug.debug("Set basename: '" + str(build_system_base_name) + "'")

def get_build_system_base_name():
	global build_system_base_name
	return build_system_base_name


def end_with(name, list):
	for appl in list:
		#debug.info("pppppppp : " + str([name[-len(appl):], appl]))
		if name[-len(appl):] == appl:
			return True
	return False

print_pretty_mode = True

def print_pretty(my_string, force=False):
	global print_pretty_mode
	if    print_pretty_mode == True \
	   or force == True:
		if my_string[len(my_string)-1] == ' ':
			tmpcmdLine = my_string[:len(my_string)-1]
		else:
			tmpcmdLine = my_string
		cmdApplication = tmpcmdLine.split(' ')[0]
		tmpcmdLine = tmpcmdLine.replace(' ', '\n\t')
		tmpcmdLine = tmpcmdLine.replace('\n\t\n\t', '\n\t')
		tmpcmdLine = tmpcmdLine.replace('\n\t\n\t', '\n\t')
		tmpcmdLine = tmpcmdLine.replace('\n\t\n\t', '\n\t')
		baseElementList = []
		if end_with(cmdApplication, ["javac"]) == True:
			baseElementList = [
			    "-d",
			    "-D",
			    "-classpath",
			    "-sourcepath"
			    ]
		elif end_with(cmdApplication, ["java"]) == True:
			baseElementList = [
			    "-z",
			    "-f",
			    "-rf"
			    ]
		elif end_with(cmdApplication, ["jarsigner"]) == True:
			baseElementList = [
			    "-sigalg",
			    "-digestalg",
			    "-storepass",
			    "-keypass"
			    ]
		elif end_with(cmdApplication, ["jar"]) == True:
			baseElementList = [
			    "cf",
			    "-C"
			    ]
		elif end_with(cmdApplication, ["aapt"]) == True:
			baseElementList = [
			    "-M",
			    "-F",
			    "-I",
			    "-S",
			    "-J"
			    ]
		elif end_with(cmdApplication, ["g++", "gcc", "clang", "clang++", "ar", "ld", "ranlib"]) == True:
			baseElementList = [
			    "-o",
			    "-D",
			    "-I",
			    "-L",
			    "-framework",
			    "-isysroot",
			    "-arch",
			    "-keystore",
			    "-sigalg",
			    "-digestalg",
			    "-target",
			    "-gcc-toolchain",
			    "-current_version",
			    "-compatibility_version"
			    ]

		for element in baseElementList:
			tmpcmdLine = tmpcmdLine.replace(element+'\n\t', element+' ')
		for element in ["<", "<<", ">", ">>"]:
			tmpcmdLine = tmpcmdLine.replace(element+'\n\t', element+' ')
		tmpcmdLine = tmpcmdLine.replace('\n\t', ' \\\n\t')
		
		return tmpcmdLine
	else:
		return my_string


