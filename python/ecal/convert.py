#!/usr/bin/python3
import os
import argparse
import struct
from pprint import pprint
import cv2
from cv_bridge import CvBridge
import ecal.measurement.measurement as Measurement
import ecal.measurement.hdf5 as ecalhdf5
import dv_processing as dv


class Event:
    def __init__(self, timestamp_sec=0, timestamp_nanosec=0, x=0, y=0, polarity=False):
        self.timestamp_sec = timestamp_sec
        self.timestamp_nanosec = timestamp_nanosec
        self.x = x
        self.y = y
        self.polarity = polarity
        

    def __repr__(self):
        return f"Event(timestamp={self.timestamp_sec}.{self.timestamp_nanosec}, x={self.x}, y={self.y}, polarity={self.polarity})"


class EcalFileParser:
    def __init__(self, ecal_file):
        self.ecal_file = ecal_file
        self.measurement = ecalhdf5.Meas(ecal_file, 0)
        # Initialize AEDAT4 output file using DV Processing library
        # self.aedat4_writer = AedatFileWriter('/home/hs/ecal_meas/rosbag2_2024_09_12-04_45_53/output3.aedat4')

        # Sample VGA resolution, same as the DVXplorer camera
        self.resolution = (640, 480)

        # Event only configuration
        self.config = dv.io.MonoCameraWriter.EventOnlyConfig("DVXplorer_sample", self.resolution)

          # Create the writer instance, it will only have a single event output stream
        self.writer = dv.io.MonoCameraWriter("/home/hs/ecal_meas/2024-09-11_07-59-31.205_measurement/output3.aedat4", self.config)


    def deserialize_message(self, ID):
        """Deserialize the incoming event array message."""
        event_array = []

        # Get entry data size
        entry_size = self.measurement.get_entry_data_size(ID)
        if entry_size <= 0:
            print("Error Getting Entry Data Size")
            return event_array

        # Get entry data
        data = self.measurement.get_entry_data(ID)
        if not data:
            print("Problem getting entry data:", ID)
            return event_array

        # Deserialize the event data
        header_format = "2I"  # Assuming height and width are uint32
        header_size = struct.calcsize(header_format)
        event_format = 'HHII?'  # x, y (uint16), time_sec, time_nanosec, polarity (bool)
        event_size = struct.calcsize(event_format)

        # Extract event data
        events_data = data[header_size+56:]  # Adjust offset as needed
        num_events = len(events_data) // event_size

        for i in range(num_events):
            event_data = events_data[i * event_size:(i + 1) * event_size]
            x, y, time_sec, time_nanosec, polarity = struct.unpack(event_format, event_data)

            event = dv.Event(self.convert_to_timestamp(time_sec, time_nanosec), x=x, y=y, polarity=polarity)
            event_array.append(event)

        print("DONE DESERIALIZING")
        return event_array

    def convert_to_timestamp(self, sec, nanosec):
        """
        Convert ROS time (seconds and nanoseconds) to a timestamp in milliseconds.
        """
        return int( (sec * 1e9) + (nanosec))

    def write_events(self, event_array):
        """Write the event array to the AEDAT4 file using the writer."""
        events = dv.EventStore()

        # Sort the event array by timestamp
        # event_array_sorted = sorted(event_array, key=lambda e: (e.timestamp_sec, e.timestamp_nanosec))

        # Write each event to the store
        for event in event_array:
            # print(event)
            events.push_back(event)

        # Write the events using the writer
        try:
            self.writer.writeEvents(events)
        except struct.error as e:
            print(f"Writing error: {e}")

    def save_events(self, topic, output_dir):
        """Save events from the specified topic in the Ecal file."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"The following channels are contained in the measurement: {self.measurement.get_channel_names()}")
        
        for channel in self.measurement.get_channel_names():
            if channel == topic:
                entries_info_read = self.measurement.get_entries_info(channel)
                print(f"Entries count: {len(entries_info_read)}\n")
                for entry_read in entries_info_read:
                    entry_data_size = self.measurement.get_entry_data_size(entry_read['id'])
                    print(f"Entry {entry_read['id']} - Size: {entry_data_size} bytes")
                    msg = self.deserialize_message(entry_read['id'])
                    self.write_events(msg)
        self.writer.close()
        print("done")
        exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_ecal', type=str, required=True, help='The input Ecal file.')
    parser.add_argument('--topic', type=str, default='rt/dv/events_left', help='Only the events from topic "topic" are used for the output.')
    parser.add_argument('--output_dir', type=str, default='./output', help='Output directory to save the event array.')
    args = parser.parse_args()

    ecal_parser = EcalFileParser(args.input_ecal)
    ecal_parser.save_events(args.topic, args.output_dir)
