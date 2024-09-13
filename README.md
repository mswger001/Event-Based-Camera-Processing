

# Event-Based Camera Processing

This repository contains tools for processing event-based camera data using both Python and C++. It supports the conversion of ROS2 bag files and eCAL measurement files to AEDAT4 format, commonly used in event-based camera systems.

## Features

- Python and C++ converters for event-based camera data.
- Convert ROS2 bag files and eCAL measurement files into AEDAT4 format.
- Processes event streams from cameras like DVXplorer.

## Directory Structure

```
Event-Based-Camera-Processing/
├── c++                     # Directory for C++ files
│   ├── include             # Header files for C++ 
│   │   ├── convert.hpp      # Header for conversion functions
│   │   ├── event_converter.hpp # Header for event conversion functions
│   │   └── msgs.hpp         # Header for message structures
│   ├── src                 # Source files for C++ 
│   │   ├── convert.cpp      # Main C++ script for converting eCAL files
│   ├── CMakeLists.txt      # CMake configuration file
│   └── README.md           # C++-specific README
│
├── python                  # Directory for Python scripts
│   ├── ecal                # Directory for eCAL processing scripts
│   │   ├── convert.py      # Main Python script for processing eCAL files
│   │   └── README.md       # eCAL-specific README
│   ├── ros2                # Directory for ROS2 processing scripts
│   │   ├── convert.py      # Main Python script for processing ROS2 bag files
│   │   └── README.md       # ROS2-specific README
│   └── README.md           # Python-specific README
│
├── output                  # Directory for output files
│   ├── processed_files/     # Processed output files
│   └── logs/               # Log files for tracking processing
│
├── LICENSE                 # License for the repository
└── README.md               # Main repository README

```

Both `python/` and `c++/` directories contain specific tools for processing event-based data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

