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
        param = "x86" if self.settings.arch == "x86" else "amd64"
        vcvars = 'call "%%vs140comntools%%../../VC/vcvarsall.bat" %s' % param
        self.run("%s && cd tbb && mingw32-make" % vcvars)

    def package(self):
        self.copy("*.h", "include", "tbb/include")
        self.copy("*.lib", "lib", "tbb/build", keep_path=False)
        self.copy("*.a", "lib", "tbb/build", keep_path=False) 
        self.copy("*.dll", "bin", "tbb/build", keep_path=False)
        self.copy("*.dylib", "lib", "tbb/build", keep_path=False)
        self.copy("*.so", "lib", "tbb/build", keep_path=False)

    def package_info(self):
        self.cpp_info.libs.extend(["tbb"])
                    
