cmake_minimum_required(VERSION 3.22)

project(Sample
    VERSION 1.0.0
    LANGUAGES C CXX
    DESCRIPTION "A sample project embedding Python in C++"
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

set(Python_FIND_VIRTUALENV FIRST)

set(LIBRARY_NAME "Library" CACHE STRING "Name of the library target")
set(EXECUTABLE_NAME "main" CACHE STRING "Name of the executable target")

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

include_directories(${Python3_INCLUDE_DIRS})

add_subdirectory(src)

message(STATUS "Project: ${PROJECT_NAME} v${PROJECT_VERSION}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Python: ${Python3_EXECUTABLE} (version ${Python3_VERSION})")
