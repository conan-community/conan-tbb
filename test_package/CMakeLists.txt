set(CMAKE_CXX_COMPILER_WORKS 1)
PROJECT(TbbExample CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
ADD_EXECUTABLE(example main.cpp)
TARGET_LINK_LIBRARIES(example ${CONAN_LIBS})
