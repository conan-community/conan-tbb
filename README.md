# conan-TBB
Intel TBB computer vision package for conan package manager

The package is still not uploaded, but working in:
- Only working in Windows, MSVC14. Hardcoded compiler.
- Requires mingw32-make to be installed and in system path

Steps: 

```bash
$ git clone https://github.com/memsharded/conan-tbb.git
$ cd conan-tbb
$ conan export memsharded/testing
$ conan test_package
```

Conan re-builds the package with ``conan test_package``, if you want to re-run the test only, you can

```bash
$ conan test_package --build=never (--build=missing will also do it)
```


This is ongoing work:

- Feel free to add tests to build, specially if something fails, with a PR, so the package is better tested


