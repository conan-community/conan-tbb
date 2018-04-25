function global:_old_conan_prompt {""}
$function:_old_conan_prompt = $function:prompt
function global:prompt { write-host "(conanenv) " -nonewline; & $function:_old_conan_prompt }
$env:MINGW_HOME = "C:/Users/danimtb/.conan/data/mingw_installer/1.0/conan/stable/package/a6efb047b0173af886a36aa7f7c661f79c0ad006"
$env:CONAN_CMAKE_GENERATOR = "MinGW Makefiles"
$env:CXX = "C:/Users/danimtb/.conan/data/mingw_installer/1.0/conan/stable/package/a6efb047b0173af886a36aa7f7c661f79c0ad006/bin/g++.exe"
$env:CC = "C:/Users/danimtb/.conan/data/mingw_installer/1.0/conan/stable/package/a6efb047b0173af886a36aa7f7c661f79c0ad006/bin/gcc.exe"
$env:PATH = "C:\Users\danimtb\.conan\data\mingw_installer\1.0\conan\stable\package\a6efb047b0173af886a36aa7f7c661f79c0ad006\bin" + ";$env:PATH"