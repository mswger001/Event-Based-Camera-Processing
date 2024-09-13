#ifndef __CONVERTER_EVENT__
#define __CONVERTER_EVENT__

#include "convert.hpp"
// #include <dv-processing/data/decoder.h> // For decoding DVXplorer data
#include <dv-processing/core/core.hpp>
#include <dv-processing/core/utils.hpp>


#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#define throw_line(message) {char err[500]="";sprintf(err,"Fatal error: %s in:" __FILE__ "line:%d\n",message,__LINE__);throw err;}
#define THROW_IF_ZERO(val) {if (!val) throw_line("Value "#val"is zero");}

namespace event_camera { namespace ecal { namespace converter  {

class ConverterEvent : public event_camera::ecal::converter ::Converter 
{
public:
    // Constructor to initialize the converter with input measurement path, channel, and output path
    ConverterEvent(
        std::string meas_path,
        std::string channel_name,
        std::string out_path
    );

    ~ConverterEvent() = default;

    // Override the deserialize_message method to handle event deserialization
    virtual struct BaseMsg deserialize_message(
        eCAL::eh5::HDF5Meas* meas_,
        long long ID
    );

    // Override the process_message method to handle event data processing and saving
    virtual void process_message(struct BaseMsg* msg);

private:
    // Path to save the processed output (e.g., AEDAT4 format)
    std::string out_path;

    // Event store for handling event-based data
    dv::EventStore event_store;

    // DVXplorer event decoder
    dv::EventStoreDecoder decoder;

    // Function to save the events to an AEDAT4 file (similar to the Python version)
    void save_events_to_aedat(const std::vector<dv::Event>& events);

    // Temporary buffer for holding event data
    std::vector<uint8_t> event_buffer;

    // Placeholder for any other necessary metadata (timestamps, etc.)
};

}}} // namespaces

#endif
