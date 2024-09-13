

# Python Tools for Event-Based Camera Processing

This directory contains Python tools for converting ROS2 bag files to AEDAT4 format using the DV Processing library. The script is designed to handle event-based camera data, such as those captured by the DVXplorer camera.

## Features

- Convert event-based camera data from ROS2 bag files to AEDAT4 format.
- Event deserialization and sorting by timestamp.
- Python implementation for processing event streams.

## Requirements

- **Python 3.8+**
- **ROS2** (for working with bag files)
- **DV Processing Library**
- Additional dependencies:
  - `rclpy`
  - `rosbag2_py`
  - `dv_processing`

To install the dependencies:

```bash
pip install rclpy rosbag2_py dv-processing
```

## How to Run

1. Clone the repository and navigate to the Python directory:

```bash
git clone https://github.com/your-username/Event-Based-Camera-Processing.git
cd Event-Based-Camera-Processing/python
```

2. Modify the paths in the `convert.py` script if necessary.

3. Run the script:

```bash
python3 convert.py
```

## Code Overview

- **BagProcessor Class**:
  - Reads event data from a ROS2 bag file.
  - Deserializes the data into individual events (`x`, `y`, timestamp, polarity).
  - Sorts the events by timestamp and writes them to an AEDAT4 file using `MonoCameraWriter`.

