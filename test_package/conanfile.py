from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "memsharded")

class TBBTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "TBB/4.4.4@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.so*", "bin", "bin")
        self.copy("*.dylib", "bin", "bin")

    def test(self):
        os.chdir("bin")
        if self.settings.os == "Linux":
            self.run("LD_LIBRARY_PATH=./ ./example")
        else:
            self.run(".%sexample" % os.sep)
