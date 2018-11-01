# conan-tbb

![conan-tbb image](/images/conan-tbb.png)

[![Download](https://api.bintray.com/packages/conan-community/conan/tbb%3Aconan/images/download.svg?version=2019_U1%3Astable)](https://bintray.com/conan-community/conan/tbb%3Aconan/2019_U1%3Astable/link)
[![Build Status](https://travis-ci.org/conan-community/conan-tbb.svg?branch=stable%2F2019_U1)](https://travis-ci.org/conan-community/conan-tbb)
[![Build status](https://ci.appveyor.com/api/projects/status/jyeh443gn0l0f3bi/branch/stable/2019_U1?svg=true)](https://ci.appveyor.com/project/memsharded/conan-tbb/branch/stable/2019_U1)

[Conan.io](https://conan.io) package for [TBB](https://www.threadingbuildingblocks.org) project.

The packages generated with this *conanfile.py* can be found in [Bintray](https://bintray.com/conan-community/conan/tbb%3Aconan).

## Basic setup

    $ conan install TBB/2019_U1@conan/stable

## Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*:

    [requires]
    TBB/2019_U1@conan/stable

    [generators]
    txt
    cmake

## License

[MIT License](LICENSE)
