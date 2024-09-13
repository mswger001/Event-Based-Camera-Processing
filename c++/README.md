

# C++ Tools for Event-Based Camera Processing

This directory contains C++ tools for converting eCAL measurement files into AEDAT4 format. The tool is designed to handle event-based camera data captured by DVXplorer and other similar cameras.

## Features

- Convert eCAL measurement files to AEDAT4 format.
- C++ implementation for fast and efficient event-based camera data processing.

## Requirements

- **eCAL**: Ensure that eCAL is installed for handling eCAL measurement files.
- **DV Processing Library**: For handling event-based data.

## How to Build

To compile the C++ converter, follow these steps:

1. Clone the repository and navigate to the `c++` directory:

```bash
git clone https://github.com/your-username/Event-Based-Camera-Processing.git
cd Event-Based-Camera-Processing/c++
```

2. Compile the C++ code:

```bash
g++ -std=c++11 convert.cpp -o ecal_to_aedat4
```

3. Run the converter:

```bash
./ecal_to_aedat4 /path/to/ecal_measurement /path/to/output.aedat4
```

## Code Overview

- **Convert Function**: This function reads eCAL measurement files, extracts event data, and writes it to an AEDAT4 file.
- **Error Handling**: The code handles various exceptions, such as missing or corrupt measurement files.

---
