import os
import shutil
from conans import ConanFile, tools


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
    default_options = "shared=True"

    def configure(self):
        if not self.options.shared:
            if self.settings.os == "Windows":
                raise Exception("Intel-TBB does not support static linking in Windows")
            else:
                self.output.warn("Intel-TBB strongly discourages usage of static linkage")

    def source(self):
        tools.get("https://www.threadingbuildingblocks.org/sites/default/filessoftware_releases/"
                  "source/tbb44_20160413oss_src.tgz")
        shutil.move("tbb44_20160413oss", "tbb")

    def build(self):
        extra = "" if self.options.shared else "extra_inc=big_iron.inc"
        arch = "ia32" if self.settings.arch == "x86" else "intel64"

        use_win_bash = False
        make = tools.get_env("CONAN_MAKE_PROGRAM")

        if not make:
            if tools.which("mingw32-make"):
                make = "mingw32-make"
            elif tools.os_info.detect_windows_subsystem():
                make = "make"
                use_win_bash = True
            else:
                make = "make"

        with tools.chdir("tbb"):
            if self.settings.compiler == "Visual Studio":
                vcvars = tools.vcvars_command(self.settings)
                try:
                    self.run("%s && %s arch=%s %s" % (vcvars, make, arch, extra),
                             win_bash=use_win_bash)
                except Exception:
                    raise Exception("This package needs 'make' in the path to build")
            elif self.settings.os == "Windows" and self.settings.compiler == "gcc":  # MinGW
                self.run("%s arch=%s compiler=gcc %s" % (make, arch, extra), win_bash=use_win_bash)
            else:
                self.run("%s arch=%s %s" % (make, arch, extra))

    def package(self):
        self.copy("*COPYING", dst="licenses", keep_path=False)
        self.copy("*.h", "include", "tbb/include")
        self.copy("*", "include/tbb/compat", "tbb/include/tbb/compat")
        build_folder = "tbb/build/"
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
