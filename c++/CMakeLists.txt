cmake_minimum_required(VERSION 3.10)
set(CMAKE_FIND_PACKAGE_PREFER_CONFIG)

# Project name
project(EventBasedCameraProcessing)

# Set C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)


# Find Boost
find_package(Boost 1.82.0 REQUIRED)
find_package(OpenCV REQUIRED)

# Include directories
include_directories(${Boost_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR}/include)

# Find required packages
find_package(PCL REQUIRED)
find_package(eCAL REQUIRED)  # Ensure eCAL is properly set up
find_package(dv-processing REQUIRED)  # Ensure dv-processing is properly set up

# Include directories for PCL, eCAL, and dv-processing
include_directories(
    ${PCL_INCLUDE_DIRS}
    ${eCAL_INCLUDE_DIRS}
    ${dv-processing_INCLUDE_DIRS}
    ${OpenCV_INCLUDE_DIRS}
)

# Source files
set(SOURCES
    src/convert.cpp
    # Add more source files here if needed
)

# Header files
set(HEADERS
    include/convert.hpp
    include/event_converter.hpp
    # Add more header files here if needed
)

# Create the executable
add_executable(EventConverter src/convert.cpp ${HEADERS})

# Link libraries
target_link_libraries(EventConverter
    ${PCL_LIBRARIES}
    ${eCAL_LIBRARIES}
    ${OpenCV_LIBRARIES}
    ${dv-processing_LIBRARIES}
    ${Boost_LIBRARIES}  # Link Boost libraries as well
    
)

# Optionally, set output directories for binaries and libraries
set_target_properties(EventConverter PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
)
