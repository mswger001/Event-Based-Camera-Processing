namespace event_camera { namespace ecal { namespace converter  {


    struct BaseMsg {
        std::string ID = "123456";

        uint32_t timestamp_sec;
        uint32_t timestamp_nanosec;
    };

    struct Event : BaseMsg {

        uint32_t height;
        uint32_t width;

        std::string encoding = "mono8";
        uint8_t is_bigendian;
        uint32_t step;

        uint64_t data_size;
        uint8_t* data;
    };



    
}}} 

// # A DVS event
// uint16 x    # pixel x coordinate
// uint16 y    # pixel y coordinate
// builtin_interfaces/Time ts
// bool polarity

// # This message contains an array of events
// # (0, 0) is at the top left corner of image

// std_msgs/Header header
// uint32 height           # image height, that is, number of rows
// uint32 width            # image width, that is, number of columns
// Event[] events          # an array of events