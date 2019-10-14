[![Download](https://api.bintray.com/packages/conan/public-conan/TBB%3Aconan/images/download.svg) ](https://bintray.com/conan/public-conan/TBB%3Aconan/_latestVersion)
[![Build Status](https://travis-ci.org/conan/conan-TBB.svg?branch=stable%2F2019_U9)](https://travis-ci.org/conan/conan-TBB)
[![Build status](https://ci.appveyor.com/api/projects/status/github/conan/conan-TBB?branch=stable%2F2019_U9&svg=true)](https://ci.appveyor.com/project/conan/conan-TBB)

[Conan.io](https://conan.io) package recipe for [*TBB*](https://github.com/01org/tbb).

Intel Threading Building Blocks (Intel TBB) lets you easily write parallel C++
programs that take full advantage of multicore performance, that are portable and composable, and
that have future-proof scalability

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/conan/public-conan/TBB%3Aconan).

## For Users: Use this package

### Basic setup

    $ conan install TBB/2019_U9@conan/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    TBB/2019_U9@conan/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to conan conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create conan/stable


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| shared      | False |  [True, False] |
| tbbmalloc      | False |  [True, False] |
| tbbproxy      | False |  [True, False] |

## Add Remote

    $ conan remote add conan "https://api.bintray.com/conan/conan/public-conan"

## Upload

    $ conan upload TBB/2019_U9@conan/stable --all -r conan


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package TBB.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/conan-community/conan-tbb.git/blob/testing/2019_U9/LICENSE.md)
