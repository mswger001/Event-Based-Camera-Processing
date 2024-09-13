
# Ecal File Event Parser

This Python script is designed to parse Ecal files and extract event data from specified topics. It deserializes the event messages and saves them in the AEDAT4 format using the DV Processing library.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [License](#license)

## Features

- Read event data from Ecal files.
- Deserialize event messages into a structured format.
- Save extracted events into the AEDAT4 format.
- Support for custom topics and output directories.

## Requirements

- Python 3.x
- Required libraries:
  - OpenCV (`cv2`)
  - `cv_bridge`
  - `ecal`
  - `dv_processing`
  
You can install the required libraries using pip:

```bash
pip install opencv-python cv_bridge ecal dv_processing
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install the necessary dependencies listed in the requirements section.

## Usage

To run the script, use the following command in your terminal:

```bash
python ecal_file_parser.py --input_ecal <path_to_ecal_file> --topic <event_topic> --output_dir <output_directory>
```

### Arguments

- `--input_ecal`: Path to the input Ecal file (required).
- `--topic`: The specific topic to extract events from (default: `rt/dv/events_left`).
- `--output_dir`: Directory to save the output event array (default: `./output`).

### Example

```bash
python ecal_file_parser.py --input_ecal /path/to/ecal/file --topic rt/dv/events_left --output_dir ./output
```

## Code Structure

- `Event`: A class representing individual event data with attributes for timestamp, coordinates, and polarity.
- `EcalFileParser`: A class that handles:
  - Loading Ecal files.
  - Deserializing event messages.
  - Writing events to AEDAT4 files.
  
### Key Functions

- `deserialize_message(ID)`: Deserializes a message with the given ID from the Ecal file.
- `convert_to_timestamp(sec, nanosec)`: Converts ROS time format to a timestamp in milliseconds.
- `write_events(event_array)`: Writes an array of events to the AEDAT4 file.
- `save_events(topic, output_dir)`: Saves events from the specified topic to the output directory.

