#include "convert.hpp"
#include <dv-processing/core/core.hpp>
#include <dv-processing/core/utils.hpp>

#include <iostream>
#include <fstream>
#include <vector>

int main(int argc, char* argv[]) {
    // Check if the correct number of arguments is provided
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <measurement_path> <channel_name> <output_path>" << std::endl;
        return 1; // Return with an error code
    }

    std::string meas_path = argv[1];
    std::string channel_name = argv[2];
    std::string out_path = argv[3];

    // Create an instance of ConverterEvent
    event_camera::ecal::converter::ConverterEvent converter(meas_path, channel_name, out_path);

    // Process all messages in the measurement file
   // converter.process_all();

    return 0; // Successful execution
}
namespace event_camera { namespace ecal { namespace converter  {

ConverterEvent::ConverterEvent(
    std::string meas_path,
    std::string channel_name,
    std::string out_path
) : Converter(meas_path, channel_name), out_path(out_path) {
    // Initialize the event decoder
    decoder = dv::EventStoreDecoder();
}

struct BaseMsg ConverterEvent::deserialize_message(
    eCAL::eh5::HDF5Meas* meas_,
    long long ID
) {
    // Initialize a message for storing the event data
    BaseMsg msg;

    // Locate the specific entry based on the ID from the HDF5 file
    eCAL::eh5::Entry entry = meas_->GetEntry(ID);

    // Decode the event data using the DV event decoder
    event_buffer = entry.Data;
    event_store = decoder.decode(event_buffer);

    // Populate the BaseMsg struct with relevant event information
    msg.timestamp = event_store.timestamp().count();
    msg.data = event_store.getEvents();

    return msg;
}

void ConverterEvent::process_message(struct BaseMsg* msg) {
    // Convert the event data to a format (e.g., AEDAT4) or other processing

    std::vector<dv::Event> events = msg->data;

    // For now, just print out some basic information
    std::cout << "Processing message with " << events.size() << " events." << std::endl;

    // Save the events to an AEDAT4 file
    save_events_to_aedat(events);
}

void ConverterEvent::save_events_to_aedat(const std::vector<dv::Event>& events) {
    // Open the output AEDAT file for writing
    std::ofstream aedat_file(out_path, std::ios::binary);

    if (!aedat_file.is_open()) {
        throw_line("Unable to open AEDAT file for writing.");
    }

    // Write the events in AEDAT4 format
    for (const auto& event : events) {
        // Write each event to the file
        aedat_file.write(reinterpret_cast<const char*>(&event), sizeof(event));
    }

    aedat_file.close();
    std::cout << "Saved " << events.size() << " events to " << out_path << std::endl;
}

}}}  // namespace event_camera -> ecal -> converter
