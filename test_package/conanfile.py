from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "memsharded")

class TBBTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "TBB/4.4.4@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.so*", "bin", "lib")
        self.copy("*.dylib", "bin", "lib")

    def test(self):
        os.chdir("bin")
        if self.settings.os != "Windows":
            self.run("LD_LIBRARY_PATH=./ ./example")
        else:
            self.run(".%sexample" % os.sep)
