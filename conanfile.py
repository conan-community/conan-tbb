# -*- coding: utf-8 -*-

from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
import os
import shutil
import tempfile


class TBBConan(ConanFile):
    name = "TBB"
    version = "4.4.4"
    license = "GPLv2 with the (libstdc++) runtime exception"
    homepage = "https://www.threadingbuildingblocks.org"
    description = """Intel Threading Building Blocks (Intel TBB) lets you easily write parallel C++
programs that take full advantage of multicore performance, that are portable and composable, and
that have future-proof scalability"""
    url = "https://github.com/conan-community/conan-tbb"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    # TBB by default is a special case, it strongly recommends SHARED
    default_options = {
        "shared": True,
    }
    _source_subfolder = "sources"

    def configure(self):
        if not self.options.shared:
            if self.settings.os == "Windows":
                raise ConanInvalidConfiguration("Intel-TBB does not support static linking in Windows")
            else:
                self.output.warn("Intel-TBB strongly discourages usage of static linkage")

    def source(self):
        filename = "tbb44_20160413oss_src.tar.gz"
        url = "https://www.threadingbuildingblocks.org/sites/default/files/software_releases/" \
              "source/tbb44_20160413oss_src.tgz"
        sha256 = "3fecffef5e42f9f22e51a81a1bfa89ea40cefb439d168c285c9d5f0128353644"

        dlfilepath = os.path.join(tempfile.gettempdir(), filename)
        if os.path.exists(dlfilepath) and not tools.get_env("TBB_FORCE_DOWNLOAD", False):
            self.output.info("Skipping download. Using cached {}".format(dlfilepath))
        else:
            self.output.info("Downloading {} from {}".format(self.name, url))
            tools.download(url, dlfilepath)
        tools.check_sha256(dlfilepath, sha256)
        tools.untargz(dlfilepath)
        extracted_dir = "tbb44_20160413oss".format(self.name, self.version)
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        extra = "" if self.options.shared else "extra_inc=big_iron.inc"
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
                    raise Exception("This package needs 'make' in the path to build")
            elif self.settings.os == "Windows" and self.settings.compiler == "gcc":  # MinGW
                self.run("%s arch=%s compiler=gcc %s" % (make, arch, extra))
            else:
                self.run("%s arch=%s %s" % (make, arch, extra))

    def package(self):
        self.copy("*COPYING", dst="licenses", keep_path=False)
        self.copy("*.h", "include", os.path.join(self._source_subfolder, "include"))
        self.copy("*", "include/tbb/compat", os.path.join(self._source_subfolder, "include", "tbb", "compat"))
        build_folder = os.path.join(self._source_subfolder, "build")
        build_type = "debug" if self.settings.build_type == "Debug" else "release"
        self.copy("*%s*.lib" % build_type, dst="lib", src=build_folder, keep_path=False)
        self.copy("*%s*.a" % build_type, dst="lib", src=build_folder, keep_path=False)
        self.copy("*%s*.dll" % build_type, dst="bin", src=build_folder, keep_path=False)
        self.copy("*%s*.dylib" % build_type, dst="lib", src=build_folder, keep_path=False)
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
            if self.options.shared:
                self.cpp_info.libs.extend(["tbbmalloc_proxy_debug"])
        else:
            self.cpp_info.libs.extend(["tbb", "tbbmalloc"])
            if self.options.shared:
                self.cpp_info.libs.extend(["tbbmalloc_proxy"])

        if not self.options.shared and self.settings.os != "Windows":
            self.cpp_info.libs.extend(["pthread"])
