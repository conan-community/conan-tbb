#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools
from conans.errors import ConanException


class TBBConan(ConanFile):
    name = "TBB"
    version = "2019_U1"
    license = "Apache-2.0"
    url = "https://github.com/conan-community/conan-tbb"
    homepage = "https://github.com/01org/tbb"
    description = """Intel Threading Building Blocks (Intel TBB) lets you easily write parallel C++
programs that take full advantage of multicore performance, that are portable and composable, and
that have future-proof scalability"""
    author = "Conan Community"
    topics = ("conan", "tbb", "threading", "parallelism", "tbbmalloc")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared

    def configure(self):
        if self.settings.os != "Windows" and self.options.shared:
            self.output.warn("Intel-TBB strongly discourages usage of static linkage")

    def source(self):
        tools.get("{}/archive/{}.tar.gz".format(self.homepage, self.version))
        os.rename("{}-{}".format(self.name.lower(), self.version), self._source_subfolder)

    def build(self):
        extra = "" if self.settings.os != "Windows" and self.options.shared else "extra_inc=big_iron.inc"
        arch = "ia32" if self.settings.arch == "x86" else "intel64"

        make = tools.get_env("CONAN_MAKE_PROGRAM", "make")

        if tools.which("mingw32-make"):
            make = "mingw32-make"

        with tools.chdir(self._source_subfolder):
            if self.settings.compiler == "Visual Studio":
                vcvars = tools.vcvars_command(self.settings)
                try:
                    self.run("%s && %s arch=%s %s" % (vcvars, make, arch, extra))
                except Exception:
                    raise ConanException("This package needs 'make' in the path to build")
            elif self.settings.os == "Windows" and self.settings.compiler == "gcc":  # MinGW
                self.run("%s arch=%s compiler=gcc %s" % (make, arch, extra))
            else:
                self.run("%s arch=%s %s" % (make, arch, extra))

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.h", dst="include", src="%s/include" % self._source_subfolder)
        self.copy(pattern="*", dst="include/tbb/compat", src="%s/include/tbb/compat" % self._source_subfolder)
        build_folder = "%s/build/" % self._source_subfolder
        build_type = "debug" if self.settings.build_type == "Debug" else "release"
        self.copy(pattern="*%s*.lib" % build_type, dst="lib", src=build_folder, keep_path=False)
        self.copy(pattern="*%s*.a" % build_type, dst="lib", src=build_folder, keep_path=False)
        self.copy(pattern="*%s*.dll" % build_type, dst="bin", src=build_folder, keep_path=False)
        self.copy(pattern="*%s*.dylib" % build_type, dst="lib", src=build_folder, keep_path=False)
        # Copy also .dlls to lib folder so consumers can link against them directly when using MinGW
        if self.settings.os == "Windows" and self.settings.compiler == "gcc":
            self.copy("*%s*.dll" % build_type, dst="lib", src=build_folder, keep_path=False)

        if self.settings.os == "Linux":
            # leaving the below line in case MacOSX build also produces the same bad libs
            extension = "dylib" if self.settings.os == "Macos" else "so"
            if self.options.shared:
                self.copy("*%s*.%s.*" % (build_type, extension), "lib", build_folder,
                          keep_path=False)
                outputlibdir = os.path.join(self.package_folder, "lib")
                os.chdir(outputlibdir)
                for fpath in os.listdir(outputlibdir):
                    self.run("ln -s \"%s\" \"%s\"" %
                             (fpath, fpath[0:fpath.rfind("." + extension) + len(extension) + 1]))

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs.extend(["tbb_debug", "tbbmalloc_debug"])
            if self.settings.os != "Windows" and self.options.shared:
                self.cpp_info.libs.extend(["tbbmalloc_proxy_debug"])
        else:
            self.cpp_info.libs.extend(["tbb", "tbbmalloc"])
            if self.settings.os != "Windows" and self.options.shared:
                self.cpp_info.libs.extend(["tbbmalloc_proxy"])

        if self.settings.os != "Windows" and not self.options.shared:
            self.cpp_info.libs.extend(["pthread"])
