from conans import ConanFile, CMake, tools
import os


class TBBConan(ConanFile):
    name = "TBB"
    version = "4.4.4"
    license = "GPLv2 with the (libstdc++) runtime exception"
    url = "https://github.com/memsharded/conan-tbb.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        tools.download("https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/tbb44_20160413oss_src.tgz", "tbb.zip")
        tools.untargz("tbb.zip")
        os.unlink("tbb.zip")
        shutil.move("tbb44_20160413oss", "tbb")
     
    def build(self):
        arch="ia32" if self.settings.arch=="x86" else "intel64"
        if self.settings.compiler == "Visual Studio":
            param = "x86" if self.settings.arch == "x86" else "amd64"
            vcvars = 'call "%%vs%s0comntools%%../../VC/vcvarsall.bat" %s' % (self.settings.compiler.version, param)     
            self.run("%s && cd tbb && mingw32-make arch=%s" % (vcvars, arch))
        else:
           self.run("cd tbb && make arch=%s" % ( arch)) 

    def package(self):
        self.copy("*.h", "include", "tbb/include")
        build_folder = "tbb/build/"
        build_type = "debug" if self.settings.build_type == "Debug" else "release"
        self.copy("*%s*.lib" % build_type, "lib", build_folder, keep_path=False)
        self.copy("*%s*.a" % build_type, "lib", build_folder, keep_path=False) 
        self.copy("*%s*.dll" % build_type, "bin", build_folder, keep_path=False)
        self.copy("*%s*.dylib" % build_type, "lib", build_folder, keep_path=False)
        self.copy("*%s*.so" % build_type, "lib", build_folder, keep_path=False)

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs.extend(["tbb_debug", "tbbmalloc_debug", "tbbmalloc_proxy_debug"])
        else:
            self.cpp_info.libs.extend(["tbb", "tbbmalloc", "tbbmalloc_proxy"])             
