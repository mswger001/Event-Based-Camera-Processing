import rclpy
from rclpy.node import Node
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions
import dv_processing as dv
import struct
import os


class BagProcessor(Node):
    def __init__(self):
        super().__init__('bag_processor')

# Define the path to the bag file
        bag_file_path = '/home/hs/ecal_meas/rosbag2_2024_09_12-05_22_39/rosbag2_2024_09_12-14_12_07/rosbag2_2024_09_12-14_12_07_0.db3'

        # Check if the file exists
        if not os.path.exists(bag_file_path):
            self.get_logger().error(f"Bag file does not exist at path: {bag_file_path}")
            return

        # Initialize StorageOptions and ConverterOptions for reading
        storage_options_read = StorageOptions(uri=bag_file_path, storage_id='sqlite3')
        converter_options_read = ConverterOptions()

          # Create the SequentialReader and open the bag file
        self.reader = SequentialReader()
        self.reader.open(storage_options_read, converter_options_read)

        # Initialize AEDAT4 output file using DV Processing library
        # self.aedat4_writer = AedatFileWriter('/home/hs/ecal_meas/rosbag2_2024_09_12-04_45_53/output3.aedat4')

        # Sample VGA resolution, same as the DVXplorer camera
        self.resolution = (640, 480)

        # Event only configuration
        self.config = dv.io.MonoCameraWriter.EventOnlyConfig("DVXplorer_sample", self.resolution)

        # Create the writer instance, it will only have a single event output stream
        self.writer = dv.io.MonoCameraWriter("/home/hs/ecal_meas/rosbag2_2024_09_12-04_45_53/output3.aedat4", self.config)

        # Process each topic in the bag
        while self.reader.has_next():
            topic, msg, timestamp = self.reader.read_next()

            # Assuming topic is related to event camera data
            if topic == '/dv/events_left':
                ds_msg = self.deserialize_event_array(msg)
                # Write the events to the AEDAT4 file
                self.write_events(ds_msg)

        # Close the writer, which will flush the data
        self.writer.close()
        print("Processing complete.")

    def deserialize_event_array(self, msg):
        """Deserialize the incoming ROS 2 event array message."""
        event_array = []
        
        header_format = "2I"# Assuming height and width are uint32
        header_size = struct.calcsize(header_format)
 
    
        event_format = 'HHII?'  # x, y (uint16), time_sec, time_nanosec, polarity (bool)
        event_size = struct.calcsize(event_format)

        # Assuming msg contains a bytearray after the header
        events_data = msg[header_size+56:]
        num_events = len(events_data) // event_size

        for i in range(num_events):
            event_data = events_data[i * event_size:(i + 1) * event_size]
            x, y, time_sec, time_nanosec, polarity = struct.unpack(event_format, event_data)

            # Create an event with a timestamp in milliseconds
            timestamp = self.convert_to_timestamp(time_sec, time_nanosec)
            
                    
            event = dv.Event(timestamp, x, y, polarity)
            

            event_array.append(event)

        return event_array

    def convert_to_timestamp(self, sec, nanosec):
        """
        Convert ROS time (seconds and nanoseconds) to a timestamp in milliseconds.
        """
        return int( (sec * 1e9) + (nanosec))//10000

    def write_events(self, event_array):
        """Write the event array to the AEDAT4 file using the writer."""
          # We can create an empty event store for the current timestamp
        events = dv.EventStore()
        # Write each event to the writer

        

        # Sort the event array by timestamp
        try:
            event_array_sorted = sorted(event_array, key=lambda event: event.timestamp())
        except TypeError as e:
            print("Error during sorting:", e)
            return

        # Write each event to the writer
        for event in event_array_sorted:
          
            # print(event.timestamp)
            events.push_back(event)  # Add the event to the store
          
        print(events.timestamps())

        # Write the packet using the writer
        try:
            self.writer.writeEvents(events)
        except struct.error as e:
            self.get_logger().error(f"writting error: {e}")


def main():
    rclpy.init()
    bag_processor = BagProcessor()
    rclpy.spin(bag_processor)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
