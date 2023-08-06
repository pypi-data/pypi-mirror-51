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
from lutin import image
from lutin import multiprocess
from lutin import host
from lutin import depend
import os
import sys

class Target(target.Target):
	def __init__(self, config, sub_name=[]):
		#processor type selection (auto/arm/ppc/x86)
		if config["arch"] == "auto":
			config["arch"] = "arm"
		#bus size selection (auto/32/64)
		if config["bus-size"] == "auto":
			config["bus-size"] = "32"
		self.type_arch = ""
		target.Target.__init__(self, ["Android"] + sub_name, config, self.type_arch)
		
		if config["bus-size"] == "32":
			self.type_arch="armv7"
		else:
			self.type_arch="arm64"
		
		self.path_ndk = os.getenv('PROJECT_NDK', "AUTO")
		self.path_sdk = os.getenv('PROJECT_SDK', "AUTO")
		# auto search NDK
		if self.path_ndk == "AUTO":
			for path in os.listdir("."):
				if os.path.isdir(path)==True:
					if path=="android":
						self.path_ndk = path + "/ndk"
			if self.path_ndk == "AUTO":
				self.path_ndk = tools.get_run_path() + "/../android/ndk"
		# auto search SDK
		if self.path_sdk == "AUTO":
			for path in os.listdir("."):
				if os.path.isdir(path)==True:
					if path=="android":
						self.path_sdk = path + "/sdk"
			if self.path_sdk == "AUTO":
				self.path_sdk = tools.get_run_path() + "/../android/sdk"
		
		if not os.path.isdir(self.path_ndk):
			debug.error("NDK path not set !!! set env : PROJECT_NDK on the NDK path")
		if not os.path.isdir(self.path_sdk):
			debug.error("SDK path not set !!! set env : PROJECT_SDK on the SDK path")
		
		
		tmpOsVal = "64"
		gccVersion = "4.9"
		# TODO : Remove this or set it better ...
		self.compilator_version = gccVersion
		if host.BUS_SIZE==64:
			tmpOsVal = "_64"
		if self.config["compilator"] == "clang":
			self.set_cross_base(self.path_ndk + "/toolchains/llvm-3.6/prebuilt/linux-x86" + tmpOsVal + "/bin/")
			# Patch for LLVM AR tool
			self.ar = self.cross + "llvm-ar"
		else:
			basepathArm = self.path_ndk + "/toolchains/arm-linux-androideabi-" + gccVersion + "/prebuilt/linux-x86" + tmpOsVal + "/bin/"
			basepathMips = self.path_ndk + "/toolchains/mipsel-linux-android-" + gccVersion + "/prebuilt/linux-x86" + tmpOsVal + "/bin/"
			basepathX86 = self.path_ndk + "/toolchains/x86-" + gccVersion + "/prebuilt/linux-x86" + tmpOsVal + "/bin/"
			self.set_cross_base(basepathArm + "arm-linux-androideabi-")
			if not os.path.isdir(basepathArm):
				debug.error("Gcc Arm path does not exist !!!")
			if not os.path.isdir(basepathMips):
				debug.info("Gcc Mips path does not exist !!!")
			if not os.path.isdir(basepathX86):
				debug.info("Gcc x86 path does not exist !!!")
		
		# TODO : Set it back in the package only ...
		#self.path_bin="mustNotCreateBinary"
		#self.path_lib="data/lib/armeabi"
		#self.path_data="data/assets"
		#self.path_doc="doc"
		#self.suffix_package='.pkg'
		self.pkg_path_data = "data/assets"
		self.pkg_path_bin = "mustNotCreateBinary"
		self.pkg_path_lib = "data/lib/armeabi"
		self.pkg_path_license = "license"
		
		# If the env variable is not define, find the newest version of the BOARD_ID (Note: 0: autofind)
		self.board_id = int(os.getenv('PROJECT_NDK_BOARD_ID', "0"))
		if self.board_id != 0:
			# check if element existed :
			if not os.path.isdir(self.path_sdk +"/platforms/android-" + str(self.board_id)):
				debug.error("Specify PROJECT_NDK_BOARD_ID env variable and the BOARD_ID does not exit ... : " + str(self.board_id) + "==> auto-search")
				self.board_id = 0
		if self.board_id == 0:
			debug.debug("Auto-search BOARD-ID")
			for iii in reversed(range(0, 50)):
				debug.debug("try: " + os.path.join(self.path_sdk, "platforms", "android-" + str(iii)))
				if os.path.isdir(os.path.join(self.path_sdk, "platforms", "android-" + str(iii))):
					debug.debug("Find BOARD-ID : " + str(iii))
					self.board_id = iii
					break;
		if self.board_id == 0:
			debug.error("Can not find BOARD-ID ==> update your android SDK")
		
		self.add_flag("c", "-D__ANDROID_BOARD_ID__=" + str(self.board_id))
		if self.type_arch == "armv5" or self.type_arch == "armv7":
			self.global_include_cc.append("-I" + os.path.join(self.path_ndk, "platforms", "android-" + str(self.board_id), "arch-arm", "usr", "include"))
		elif self.type_arch == "mips":
			self.global_include_cc.append("-I" + os.path.join(self.path_ndk, "platforms", "android-" + str(self.board_id), "arch-mips", "usr", "include"))
		elif self.type_arch == "x86":
			self.global_include_cc.append("-I" + os.path.join(self.path_ndk, "platforms", "android-" + str(self.board_id), "arch-x86", "usr", "include"))
		
		self.global_include_cc.append("-I" + os.path.join(self.path_ndk, "sources", "android", "support", "include"))
		
		if self.config["compilator"] == "clang":
			self.global_include_cc.append("-gcc-toolchain " + os.path.join(self.path_ndk, "sources", "android", "support", "include"))
			if self.type_arch == "armv5":
				pass
			elif self.type_arch == "armv7":
				# The only one tested ... ==> but we have link error ...
				self.add_flag("c", [
				    "-target armv7-none-linux-androideabi",
				    "-march=armv7-a",
				    "-mfpu=vfpv3-d16",
				    "-mhard-float"
				    ])
				self.add_flag("link", [
				    "-target armv7-none-linux-androideabi",
				    "-Wl,--fix-cortex-a8",
				    "-Wl,--no-warn-mismatch",
				    "-lm_hard"
				    ])
			elif self.type_arch == "mips":
				pass
			elif self.type_arch == "x86":
				pass
		else:
			if self.type_arch == "armv5":
				pass
			elif self.type_arch == "armv7":
				pass
			elif self.type_arch == "mips":
				pass
			elif self.type_arch == "x86":
				pass
		
		self.sysroot = "--sysroot=" + os.path.join(self.path_ndk, "platforms", "android-" + str(self.board_id), "arch-arm")
		
		if True:
			self._mode_arm = "thumb"
		else:
			self._mode_arm = "arm"
		
		
		self.add_flag("c", [
		    "-D__ARM_ARCH_5__",
		    "-D__ARM_ARCH_5T__",
		    "-D__ARM_ARCH_5E__",
		    "-D__ARM_ARCH_5TE__"
		    ])
		if self.config["compilator"] != "clang":
			if self.type_arch == "armv5":
				# -----------------------
				# -- arm V5 :
				# -----------------------
				self.add_flag("c", [
				    "-march=armv5te",
				    "-msoft-float"
				    ])
			else:
				# -----------------------
				# -- arm V7 (Neon) :
				# -----------------------
				self.add_flag("c", [
				    "-m"+self._mode_arm,
				    "-mfpu=neon",
				    "-march=armv7-a",
				    "-mtune=cortex-a8",
				    "-mfloat-abi=softfp",
				    "-mvectorize-with-neon-quad",
				    "-D__ARM_ARCH_7__",
				    "-D__ARM_NEON__"
				    ])
				self.add_flag("link", [
				    "-mfpu=neon",
				    "-mfloat-abi=softfp",
				    "-Wl,--fix-cortex-a8",
				    ])
		"""
		self.add_flag("link-lib", [
		    "dl"
		    ])
		self.add_flag("link", [
		    "-rdynamic"
		    ])
		"""
		# the -mthumb must be set for all the android produc, some ot the not work coretly without this one ... (all android code is generated with this flags)
		#self.add_flag("c", "-mthumb")
		# -----------------------
		# -- Common flags :
		# -----------------------
		self.add_flag("c", "-fpic")
		if self.config["compilator"] != "clang":
			self.add_flag("c", [
			    "-ffunction-sections",
			    "-funwind-tables",
			    "-fstack-protector",
			    "-Wno-psabi",
			    #"-mtune=xscale",
			    "-fomit-frame-pointer",
			    "-fno-strict-aliasing"
			    ])
		self.add_flag("c++", [
		    "-frtti",
		    "-fexceptions",
		    "-Wa,--noexecstack"
		    ])
	
	##
	## @brief Get the arm mode that is build
	## @return "thumb" for thumb mode and "arm for normal mode
	##
	def get_arm_mode(self):
		return self._mode_arm
	
	def convert_name_application(self, pkg_name):
		value = pkg_name.lower()
		value = value.replace(' ', '')
		value = value.replace('-', '')
		value = value.replace('_', '')
		return value
	
	"""
	def get_staging_path_data(self, binary_name):
		return self.get_staging_path(binary_name) + self.path_data
	"""
	
	def make_package_binary(self, pkg_name, pkg_properties, base_pkg_path, heritage_list, static):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Generate package '" + pkg_name + "' v" + tools.version_to_string(pkg_properties["VERSION"]))
		debug.debug("------------------------------------------------------------------------")
		#output path
		target_outpath = self.get_staging_path(pkg_name)
		tools.create_directory_of_file(target_outpath)
		
		## Create share datas:
		self.make_package_binary_data(target_outpath, pkg_name, base_pkg_path, heritage_list, static)
		
		## copy binary files
		# in Android Package we have no binary element, only shared object ... (and java start file)
		
		## Create libraries (special case of Android...)
		copy_list={}
		target_outpath_lib = os.path.join(target_outpath, self.pkg_path_lib)
		tools.create_directory_of_file(target_outpath_lib)
		# copy application lib: (needed to lunch ...)
		file_src = self.get_build_file_dynamic(pkg_name)
		if os.path.isfile(file_src):
			debug.debug("      need copy: " + file_src + " to " + target_outpath_lib)
			tools.copy_file(file_src,
			                os.path.join(target_outpath_lib, os.path.basename(file_src)),
			                in_list=copy_list)
		# copy other if needed:
		if static == False:
			#copy all shared libsh...
			debug.verbose("libs for " + str(pkg_name) + ":")
			for heritage in heritage_list.list_heritage:
				debug.debug("sub elements: " + str(heritage.name))
				file_src = self.get_build_file_dynamic(heritage.name)
				debug.verbose("      has directory: " + file_src)
				if os.path.isfile(file_src):
					debug.debug("      need copy: " + file_src + " to " + target_outpath_lib)
					#copy all data:
					# TODO : We can have a problem when writing over library files ...
					tools.copy_file(file_src,
					                os.path.join(target_outpath_lib, os.path.basename(file_src)),
					                in_list=copy_list)
		#real copy files
		tools.copy_list(copy_list)
		if self.pkg_path_lib != "":
			# remove unneded files (NOT folder ...)
			tools.clean_directory(target_outpath_lib, copy_list)
		
		## Create generic files:
		self.make_package_generic_files(target_outpath, pkg_properties, pkg_name, base_pkg_path, heritage_list, static)
		
		## create specific android project (local)
		pkg_name_application_name = pkg_name
		if self.config["mode"] == "debug":
			pkg_name_application_name += "debug"
		#debug.info("ploppppp: " + str(pkg_properties))
		# FINAL_path_JAVA_PROJECT
		self.path_java_project = os.path.join(target_outpath,
		                                      "src")
		if pkg_properties["COMPAGNY_TYPE"] != "":
			self.path_java_project = os.path.join(self.path_java_project,
			                                      pkg_properties["COMPAGNY_TYPE"])
		if pkg_properties["COMPAGNY_NAME2"] != "":
			self.path_java_project = os.path.join(self.path_java_project,
			                                      pkg_properties["COMPAGNY_NAME2"])
		self.path_java_project = os.path.join(self.path_java_project,
		                                      pkg_name_application_name)
		#FINAL_FILE_ABSTRACTION
		self.file_final_abstraction = os.path.join(self.path_java_project, pkg_name_application_name + ".java")
		
		compleatePackageName = ""
		if pkg_properties["COMPAGNY_TYPE"] != "":
			compleatePackageName += pkg_properties["COMPAGNY_TYPE"] + "."
		if pkg_properties["COMPAGNY_NAME2"] != "":
			compleatePackageName += pkg_properties["COMPAGNY_NAME2"] + "."
		compleatePackageName += pkg_name_application_name
		
		if "ADMOD_ID" in pkg_properties:
			pkg_properties["RIGHT"].append("INTERNET")
			pkg_properties["RIGHT"].append("ACCESS_NETWORK_STATE")
		
		
		debug.print_element("pkg", "absractionFile", "<==", "dynamic file")
		# Create path :
		tools.create_directory_of_file(self.file_final_abstraction)
		# Create file :
		# java ==> done by ewol wrapper ... (and compiled in the normal compilation system ==> must be find in the dependency list of jar ...
		
		tools.create_directory_of_file(target_outpath + "/res/drawable/icon.png");
		if     "ICON" in pkg_properties.keys() \
		   and pkg_properties["ICON"] != "":
			image.resize(pkg_properties["ICON"], target_outpath + "/res/drawable/icon.png", 256, 256)
		else:
			# to be sure that we have all time a resource ...
			tmpFile = open(target_outpath + "/res/drawable/plop.txt", 'w')
			tmpFile.write('plop\n')
			tmpFile.flush()
			tmpFile.close()
		
		if pkg_properties["ANDROID_MANIFEST"]!="":
			debug.print_element("pkg", "AndroidManifest.xml", "<==", pkg_properties["ANDROID_MANIFEST"])
			tools.copy_file(pkg_properties["ANDROID_MANIFEST"], target_outpath + "/AndroidManifest.xml", force=True)
		else:
			debug.error("missing parameter 'ANDROID_MANIFEST' in the properties ... ")
		
		#add properties on wallpaper :
		# myModule.add_pkg("ANDROID_WALLPAPER_PROPERTIES", ["list", key, title, summary, [["key","value display"],["key2","value display 2"]])
		# myModule.add_pkg("ANDROID_WALLPAPER_PROPERTIES", ["list", "testpattern", "Select test pattern", "Choose which test pattern to display", [["key","value display"],["key2","value display 2"]]])
		# myModule.add_pkg("ANDROID_WALLPAPER_PROPERTIES", ["bool", key, title, summary, ["enable string", "disable String"])
		# myModule.add_pkg("ANDROID_WALLPAPER_PROPERTIES", ["bool", "movement", "Motion", "Apply movement to test pattern", ["Moving test pattern", "Still test pattern"]
		#copy needed resources :
		for res_source, res_dest in pkg_properties["ANDROID_RESOURCES"]:
			if res_source == "":
				continue
			tools.copy_file(res_source , target_outpath + "/res/" + res_dest + "/" + os.path.basename(res_source), force=True)
		
		
		# Doc :
		# http://asantoso.wordpress.com/2009/09/15/how-to-build-android-application-package-apk-from-the-command-line-using-the-sdk-tools-continuously-integrated-using-cruisecontrol/
		debug.print_element("pkg", "R.java", "<==", "Resources files")
		tools.create_directory_of_file(target_outpath + "/src/noFile")
		android_tool_path = self.path_sdk + "/build-tools/"
		# find android tool version
		dirnames = tools.get_list_sub_path(android_tool_path)
		if len(dirnames) == 0:
			debug.warning("This does not comport directory: '" + android_tool_path + "'")
			debug.error("An error occured when getting the tools for android")
		elif len(dirnames) > 1:
			dirnames = sorted(dirnames, reverse=True)
			debug.debug("sort tools directory: '" + str(dirnames) + "' ==> select : " + str(dirnames[0]))
		android_tool_path += dirnames[0] + "/"
		
		# this is to create resource file for android ... (we did not use aset in jar with ewol ...
		adModResoucepath = ""
		if "ADMOD_ID" in pkg_properties:
			adModResoucepath = " -S " + self.path_sdk + "/extras/google/google_play_services/libproject/google-play-services_lib/res/ "
		cmdLine = android_tool_path + "aapt p -f " \
		          + "-M " + target_outpath + "/AndroidManifest.xml " \
		          + "-F " + target_outpath + "/resources.res " \
		          + "-I " + self.path_sdk + "/platforms/android-" + str(self.board_id) + "/android.jar "\
		          + "-S " + target_outpath + "/res/ " \
		          + adModResoucepath \
		          + "-J " + target_outpath + "/src/ "
		multiprocess.run_command(cmdLine)
		
		tools.create_directory_of_file(target_outpath + "/build/classes/noFile")
		debug.print_element("pkg", "*.class", "<==", "*.java")
		#generate android java files:
		filesString=""
		
		"""
		old : 
		if "ADMOD_ID" in pkg_properties:
			# TODO : check this I do not think it is really usefull ... ==> write for IDE only ...
			filesString += self.path_sdk + "/extras/google/google_play_services/libproject/google-play-services_lib/src/android/UnusedStub.java "
		if len(pkg_properties["ANDROID_WALLPAPER_PROPERTIES"])!=0:
			filesString += self.path_java_project + pkg_name_application_name + "Settings.java "
		
		adModJarFile = ""
		if "ADMOD_ID" in pkg_properties:
			adModJarFile = ":" + self.path_sdk + "/extras/google/google_play_services/libproject/google-play-services_lib/libs/google-play-services.jar"
		
		cmdLine = "javac " \
		          + "-d " + self.get_staging_path(pkg_name) + "/build/classes " \
		          + "-classpath " + self.path_sdk + "/platforms/android-" + str(self.board_id) + "/android.jar" \
		          + adModJarFile + " " \
		          + filesString \
		          + self.file_final_abstraction + " "  \
		          + self.get_staging_path(pkg_name) + "/src/R.java "
		multiprocess.run_command(cmdLine)
		"""
		debug.verbose("heritage .so=" + str(tools.filter_extention(heritage_list.src['dynamic'], ["so"])))
		debug.verbose("heritage .jar=" + str(tools.filter_extention(heritage_list.src['src'], ["jar"])))
		
		class_extern = ""
		upper_jar = tools.filter_extention(heritage_list.src['src'], ["jar"])
		#debug.warning("ploppppp = " + str(upper_jar))
		for elem in upper_jar:
			if len(class_extern) > 0:
				class_extern += ":"
			class_extern += elem
		# create enpoint element :
		cmdLine = "javac " \
		          + "-d " + target_outpath + "/build/classes " \
		          + "-classpath " + class_extern + " " \
		          + target_outpath + "/src/R.java "
		multiprocess.run_command(cmdLine)
		
		debug.print_element("pkg", ".dex", "<==", "*.class")
		cmdLine = android_tool_path + "dx " \
		          + "--dex --no-strict " \
		          + "--output=" + target_outpath + "/build/" + pkg_name_application_name + ".dex " \
		          + target_outpath + "/build/classes/ "
		
		if "ADMOD_ID" in pkg_properties:
			cmdLine += self.path_sdk + "/extras/google/google_play_services/libproject/google-play-services_lib/libs/google-play-services.jar "
		# add element to dexification:
		for elem in upper_jar:
			# remove android sdk:
			if elem[-len("android.jar"):] != "android.jar":
				cmdLine += elem + " "
		
		multiprocess.run_command(cmdLine)
		
		debug.print_element("pkg", ".apk", "<==", ".dex, assets, .so, res")
		#builderDebug="-agentlib:jdwp=transport=dt_socket,server=y,address=8050,suspend=y "
		builderDebug=""
		# note : set -u not signed application...
		#+ ":" + self.path_sdk + "/extras/google/google_play_services/libproject/google-play-services_lib/libs/google-play-services.jar "
		cmdLine =   "java -Xmx128M " \
		          + " -classpath " + self.path_sdk + "/tools/lib/sdklib.jar " \
		          + builderDebug \
		          + " com.android.sdklib.build.ApkBuilderMain " \
		          + target_outpath + "/build/" + pkg_name_application_name + "-unalligned.apk " \
		          + " -u " \
		          + " -z " + target_outpath + "/resources.res " \
		          + " -f " + target_outpath + "/build/" + pkg_name_application_name + ".dex " \
		          + " -rf " + target_outpath + "/data "
		multiprocess.run_command(cmdLine)
		
		# doc :
		# http://developer.android.com/tools/publishing/app-signing.html
		# Create a key for signing your application:
		# keytool -genkeypair -v -keystore AndroidKey.jks -storepass Pass__AndroidDebugKey -alias alias__AndroidDebugKey -keypass PassKey__AndroidDebugKey -keyalg RSA -validity 36500
		if self.config["mode"] == "debug":
			debug.print_element("pkg", ".apk(signed debug)", "<==", ".apk (not signed)")
			# verbose mode : 
			#debugOption = "-verbose -certs "
			debugOption = ""
			cmdLine = "jarsigner " \
			    + debugOption \
			    + "-keystore " + tools.get_current_path(__file__) + "/AndroidDebugKey.jks " \
			    + " -sigalg SHA1withRSA -digestalg SHA1 " \
			    + " -storepass Pass__AndroidDebugKey " \
			    + " -keypass PassKey__AndroidDebugKey " \
			    + target_outpath + "/build/" + pkg_name_application_name + "-unalligned.apk " \
			    + " alias__AndroidDebugKey"
			multiprocess.run_command(cmdLine)
			tmpFile = open("tmpPass.boo", 'w')
			tmpFile.write("\n")
			tmpFile.flush()
			tmpFile.close()
		else:
			print("On release mode we need the file :  and key an pasword to sign the application ...")
			debug.print_element("pkg", ".apk(signed debug)", "<==", ".apk (not signed)")
			cmdLine = "jarsigner " \
			    + " -keystore " + pkg_properties["ANDROID_SIGN"] + " " \
			    + " -sigalg SHA1withRSA -digestalg SHA1 " \
			    + target_outpath + "/build/" + pkg_name_application_name + "-unalligned.apk " \
			    + " " + pkg_name_application_name
			multiprocess.run_command(cmdLine)
			cmdLine = "jarsigner " \
			    + " -verify -verbose -certs " \
			    + " -sigalg SHA1withRSA -digestalg SHA1 " \
			    + target_outpath + "/build/" + pkg_name_application_name + "-unalligned.apk "
			multiprocess.run_command(cmdLine)
		
		debug.print_element("pkg", ".apk(aligned)", "<==", ".apk (not aligned)")
		tools.remove_file(target_outpath + "/" + pkg_name_application_name + ".apk")
		# verbose mode : -v
		cmdLine = android_tool_path + "zipalign 4 " \
		          + target_outpath + "/build/" + pkg_name_application_name + "-unalligned.apk " \
		          + target_outpath + "/" + pkg_name_application_name + ".apk "
		multiprocess.run_command(cmdLine)
		
		# copy file in the final stage :
		tools.copy_file(target_outpath + "/" + pkg_name_application_name + ".apk",
		                self.get_final_path() + "/" + pkg_name_application_name + ".apk",
		                force=True)
	
	def install_package(self, pkg_name):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Install package '" + pkg_name + "'")
		debug.debug("------------------------------------------------------------------------")
		pkg_name_application_name = pkg_name
		if self.config["mode"] == "debug":
			pkg_name_application_name += "debug"
		cmdLine = self.path_sdk + "/platform-tools/adb install -r " \
		          + self.get_staging_path(pkg_name) + "/" + pkg_name_application_name + ".apk "
		multiprocess.run_command(cmdLine)
	
	def un_install_package(self, pkg_name):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Un-Install package '" + pkg_name + "'")
		debug.debug("------------------------------------------------------------------------")
		pkg_name_application_name = pkg_name
		if self.config["mode"] == "debug":
			pkg_name_application_name += "debug"
		cmdLine = self.path_sdk + "/platform-tools/adb uninstall " + pkg_name_application_name
		Rmultiprocess.run_command(cmdLine)
	
	def show_log(self, pkg_name):
		debug.debug("------------------------------------------------------------------------")
		debug.info("logcat of android board")
		debug.debug("------------------------------------------------------------------------")
		debug.info("cmd: " + self.path_sdk + "/platform-tools/adb shell logcat ")
		cmdLine = self.path_sdk + "/platform-tools/adb shell logcat "
		multiprocess.run_command_no_lock_out(cmdLine)


