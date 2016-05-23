PROJECT(TbbExample)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(example main.cpp)
TARGET_LINK_LIBRARIES(example ${CONAN_LIBS})
