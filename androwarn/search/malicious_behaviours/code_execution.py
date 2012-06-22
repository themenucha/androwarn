#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Androwarn.
#
# Copyright (C) 2012, Thomas Debize <tdebize at mail.com>
# All rights reserved.
#
# Androwarn is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Androwarn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Androwarn.  If not, see <http://www.gnu.org/licenses/>.

# Global imports
import os, re, logging

# Androguard imports
from androguard.core.analysis import analysis
from androguard.core.bytecodes.apk import *

# Androwarn modules import
from androwarn.core.core import *
from androwarn.util.util import *

# Logguer
log = logging.getLogger('log')


def detect_Library_loading(x) :
	"""
		@param x : a VMAnalysis instance
		
		@rtype : a list of formatted strings
	"""
	# Several HTC devices suffered from a bug allowing to dump wpa_supplicant.conf file containing clear text credentials
	formatted_str = []
	
	b = x.tainted_packages.search_methods("Ljava/lang/System","loadLibrary", ".")
	for result in xrange(len(b)) :
		method = b[result].get_method()
		method_call_index_to_find = b[result].get_idx()
		
		registers = backtrace_registers_before_call(x, method, method_call_index_to_find)
		log.info("Class '%s' - Method '%s' - register state before call %s" % (b[result].get_class_name(),b[result].get_name(), registers))
					
		local_formatted_str = "This application loads a native library" 
		
		# If we're lucky enough to directly have the library's name
		if len(registers) == 1 :
			local_formatted_str = "%s : '%s'" % (local_formatted_str, get_register_value(0, registers))
		
		# we want only one occurence
		if not(local_formatted_str in formatted_str) :
			formatted_str.append(local_formatted_str)

		
	return formatted_str


def detect_UNIX_command_execution(x) :
	"""
		@param x : a VMAnalysis instance
		
		@rtype : a list of formatted strings
	"""
	# Several HTC devices suffered from a bug allowing to dump wpa_supplicant.conf file containing clear text credentials
	formatted_str = []
	
	b = x.tainted_packages.search_methods("Ljava/lang/Runtime","exec", ".")
	for result in xrange(len(b)) :
		method = b[result].get_method()
		#method_call_index_to_find = b[result].get_offset()
		method_call_index_to_find = b[result].get_idx()
		
		registers = backtrace_registers_before_call(x, method, method_call_index_to_find)
		log.info("Class '%s' - Method '%s' - register state before call %s" % (b[result].get_class_name(),b[result].get_name(), registers))
				
		local_formatted_str = "This application executes that UNIX command" 
		
		# we want only one occurence
		if not(local_formatted_str in formatted_str) :
			formatted_str.append(local_formatted_str)

		
	return formatted_str
