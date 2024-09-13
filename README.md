

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
│   ├── convert.cpp          # Main C++ script for converting eCAL files
│   └── README.md            # C++-specific README
│
├── python                  # Directory for Python scripts
│   ├── convert.py          # Main Python script for processing bag files
│   └── README.md           # Python-specific README
│
├── LICENSE                 # License for the repository
└── README.md               # Main repository README
```

Both `python/` and `c++/` directories contain specific tools for processing event-based data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

