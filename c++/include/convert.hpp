#ifndef __CONVERTER__
#define __CONVERTER__

#include <ecalhdf5/eh5_meas.h>
#include <iostream>
#include "msgs.hpp"

namespace event_camera { namespace ecal { namespace converter {

class Converter
{
public:
    // Constructor to initialize the converter with the path and channel name
    inline explicit Converter(std::string meas_path, std::string channel_name) {
        this->meas_ = new eCAL::eh5::HDF5Meas(meas_path);
        if (!meas_->IsOk()) {
            std::cout << "Problem with measurement file." << std::endl;
        }
        this->meas_->GetEntriesInfo(channel_name, this->entry_info_set);
    }

    // Virtual destructor
    virtual ~Converter() = default;

    // Pure virtual function to deserialize a message
    virtual struct BaseMsg deserialize_message(
        eCAL::eh5::HDF5Meas* meas_,
        long long ID
    ) = 0;

    // Pure virtual function to process a message
    virtual void process_message(struct BaseMsg* msg) = 0;

    // Function to process all messages in the measurement file
    inline void process_all() {
        for (auto it = this->entry_info_set.begin(); it != this->entry_info_set.end(); it++) {
            std::cout << "-------------------------------" << std::endl;
            struct BaseMsg msg = deserialize_message(this->meas_, it->ID);
            process_message(&msg);
        }
    }

private:
    // Measurement reading variables
    eCAL::eh5::HDF5Meas* meas_;               // Pointer to the measurement object
    eCAL::eh5::EntryInfoSet entry_info_set;   // Set of entry information for the channel
};

}}}  //event_camera --> ecal --> converter


#endif
