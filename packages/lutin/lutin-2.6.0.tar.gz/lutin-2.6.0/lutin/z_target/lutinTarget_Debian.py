#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##

from realog import debug
from lutin import target
from lutin import tools
import os
import stat
import re
from lutin import depend
from lutin import host
from lutin import multiprocess
import lutinTarget_Linux

class Target(lutinTarget_Linux.Target):
	def __init__(self, config, sub_name=[]):
		lutinTarget_Linux.Target.__init__(self, config, ["Debian"] + sub_name)
	
	"""
	.local/application
	    *--> applName -> applName.app/bin/applName
	    *--> applName.app
	        *--> appl_description.txt
	        *--> appl_name.txt
	        *--> changelog.txt
	        *--> copyright.txt
	        *--> readme.txt
	        *--> version.txt
	        *--> website.txt
	        *--> icon.png
	        *--> bin
	        *    *--> applName
	        *--> doc
	        *    *--> applName
	        *--> lib
	        *    *--> XX.so
	        *    *--> YY.so
	        *--> license
	        *    *--> applName.txt
	        *    *--> libXX.txt
	        *    *--> libYY.txt
	        *--> man
	        *--> share
	        *    *--> applName
	        *    *--> XX
	        *    *--> YY
	        *--> sources
	"""
	def make_package_binary(self, pkg_name, pkg_properties, base_pkg_path, heritage_list, static):
		# http://alp.developpez.com/tutoriels/debian/creer-paquet/
		debianpkg_name = re.sub("_", "-", pkg_name)
		debug.debug("------------------------------------------------------------------------")
		debug.info("Generate generic '" + pkg_name + "' v" + tools.version_to_string(pkg_properties["VERSION"]))
		debug.debug("------------------------------------------------------------------------")
		#output path
		target_outpath = os.path.join(self.get_staging_path(pkg_name), pkg_name + ".app")
		tools.create_directory_of_file(target_outpath)
		
		## Create share datas:
		ret_share = self.make_package_binary_data(target_outpath, pkg_name, base_pkg_path, heritage_list, static)
		
		## copy binary files:
		ret_bin = self.make_package_binary_bin(target_outpath, pkg_name, base_pkg_path, heritage_list, static)
		
		## Create libraries:
		ret_lib = self.make_package_binary_lib(target_outpath, pkg_name, base_pkg_path, heritage_list, static)
		
		## Create generic files:
		ret_file = self.make_package_generic_files(target_outpath, pkg_properties, pkg_name, base_pkg_path, heritage_list, static)
		
		## end of the package generation
		build_package_path_done = os.path.join(self.get_build_path(pkg_name), "generatePackageDone.txt")
		#Check date between the current file "list of action to generate package and the end of package generation
		need_generate_package = depend.need_re_package(build_package_path_done, [__file__], True)
		
		## create the package:
		if    ret_share \
		   or ret_bin \
		   or ret_lib \
		   or ret_file \
		   or need_generate_package:
			"""
			## create the package:
			debug.debug("package : " + self.get_staging_path(pkg_name) + "/" + pkg_name + ".app.pkg")
			os.system("cd " + self.get_staging_path(pkg_name) + " ; tar -czf " + pkg_name + ".app.tar.gz " + pkg_name + ".app")
			#multiprocess.run_command("cd " + self.get_staging_path(pkg_name) + " ; tar -czf " + pkg_name + ".app.tar.gz " + pkg_name + ".app")
			tools.create_directory_of_file(self.get_final_path())
			tools.copy_file(self.get_staging_path(pkg_name) + "/" + pkg_name + ".app.tar.gz", self.get_final_path() + "/" + pkg_name + ".app.gpkg")
			def make_package_binary(self, pkg_name, pkg_properties, base_pkg_path, heritage_list, static):
			"""
			self.get_staging_path(pkg_name)
			target_outpathDebian = self.get_staging_path(pkg_name) + "/DEBIAN/"
			finalFileControl = target_outpathDebian + "control"
			finalFilepostRm = target_outpathDebian + "postrm"
			# create the paths :
			tools.create_directory_of_file(finalFileControl)
			tools.create_directory_of_file(finalFilepostRm)
			## Create the control file
			tools.create_directory_of_file(finalFileControl)
			tmpFile = open(finalFileControl, 'w')
			tmpFile.write("Package: " + debianpkg_name + "\n")
			tmpFile.write("Version: " + tools.version_to_string(pkg_properties["VERSION"]) + "\n")
			tmpFile.write("Section: " + self.generate_list_separate_coma(pkg_properties["SECTION"]) + "\n")
			tmpFile.write("Priority: " + pkg_properties["PRIORITY"] + "\n")
			tmpFile.write("Architecture: all\n")
			tmpFile.write("Depends: bash\n")
			tmpFile.write("Maintainer: " + self.generate_list_separate_coma(pkg_properties["MAINTAINER"]) + "\n")
			tmpFile.write("Description: " + pkg_properties["DESCRIPTION"] + "\n")
			tmpFile.write("\n")
			tmpFile.flush()
			tmpFile.close()
			## Create the PostRm
			tmpFile = open(finalFilepostRm, 'w')
			tmpFile.write("#!/bin/bash\n")
			tmpFile.write("touch ~/." + pkg_name + "\n")
			if pkg_name != "":
				tmpFile.write("touch ~/.local/share/" + pkg_name + "\n")
				tmpFile.write("rm -r ~/.local/share/" + pkg_name + "\n")
			tmpFile.write("\n")
			tmpFile.flush()
			tmpFile.close()
			## Enable Execution in script
			os.chmod(finalFilepostRm, stat.S_IRWXU + stat.S_IRGRP + stat.S_IXGRP + stat.S_IROTH + stat.S_IXOTH);
			## Readme donumentation
			readmeFileDest = self.get_staging_path(pkg_name) + "/usr/share/doc/"+ debianpkg_name + "/README"
			tools.create_directory_of_file(readmeFileDest)
			if os.path.exists(base_pkg_path + "/os-Linux/README")==True:
				tools.copy_file(base_pkg_path + "/os-Linux/README", readmeFileDest)
			elif os.path.exists(base_pkg_path + "/README")==True:
				tools.copy_file(base_pkg_path + "/README", readmeFileDest)
			elif os.path.exists(base_pkg_path + "/README.md")==True:
				tools.copy_file(base_pkg_path + "/README.md", readmeFileDest)
			else:
				debug.info("no file 'README', 'README.md' or 'os-Linux/README' ==> generate an empty one")
				tmpFile = open(readmeFileDest, 'w')
				tmpFile.write("No documentation for " + pkg_name + "\n")
				tmpFile.flush()
				tmpFile.close()
			## licence file
			license_file_dest = self.get_staging_path(pkg_name) + "/usr/share/doc/"+ debianpkg_name + "/copyright"
			tools.create_directory_of_file(license_file_dest)
			if os.path.exists(base_pkg_path + "/license.txt")==True:
				tools.copy_file(base_pkg_path + "/license.txt", license_file_dest)
			else:
				debug.info("no file 'license.txt' ==> generate an empty one")
				tmpFile = open(license_file_dest, 'w')
				tmpFile.write("No license define by the developper for " + pkg_name + "\n")
				tmpFile.flush()
				tmpFile.close()
			##changeLog file
			change_log_file_dest = self.get_staging_path(pkg_name) + "/usr/share/doc/"+ debianpkg_name + "/changelog"
			tools.create_directory_of_file(change_log_file_dest)
			if os.path.exists(base_pkg_path + "/changelog")==True:
				tools.copy_file(base_pkg_path + "/changelog", change_log_file_dest)
			else:
				debug.info("no file 'changelog' ==> generate an empty one")
				tmpFile = open(change_log_file_dest, 'w')
				tmpFile.write("No changelog data " + pkg_name + "\n")
				tmpFile.flush()
				tmpFile.close()
			## create the package :
			debug.debug("package : " + self.get_staging_path(pkg_name) + "/" + debianpkg_name + ".deb")
			os.system("cd " + self.get_staging_path("") + " ; dpkg-deb --build " + pkg_name)
			tools.create_directory_of_file(self.get_final_path())
			tools.copy_file(self.get_staging_path("") + "/" + pkg_name + self.suffix_package, self.get_final_path() + "/" + pkg_name + self.suffix_package)
			
			# package is done corectly ...
			tools.file_write_data(build_package_path_done, "done...")
	
	def install_package(self, pkg_name):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Install package '" + pkg_name + "'")
		debug.debug("------------------------------------------------------------------------")
		os.system("sudo dpkg -i " + self.get_final_path() + "/" + pkg_name + self.suffix_package)
	
	def un_install_package(self, pkg_name):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Un-Install package '" + pkg_name + "'")
		debug.debug("------------------------------------------------------------------------")
		os.system("sudo dpkg -r " + self.get_final_path() + "/" + pkg_name + self.suffix_package)
	


