#ifndef _CSENSOR_TEST_H_
#define _CSENSOR_TEST_H_

/*
 *  csensor-witmotion.h
 *  qcn
 *
 *  Created by Carl Christensen on 08/11/2007.
 *  Copyright 2007 Stanford University
 *
 * This file contains an example usage of the CSensor class for QCN
 */

#include "csensor.h"

#define STR_LINUX_USB_WITMOTION01     "/dev/ttyUSB*"

// this is an example declaration of a class derived from CSensor
// you probably will not need to modify CSensor -- just override the necessary functions here
class CSensorWitMotion  : public CSensor
{
   private:
        // private member vars if needed
        int m_fd;
        int ret;
        char r_buf[1024];
        float a[3],w[3],Angle[3],h[3];

        // you will need to define a read_xyz function (pure virtual function in CSensor)
        virtual bool read_xyz(float& x1, float& y1, float& z1);

   public:
        // public member vars if needed

        CSensorWitMotion();
        virtual ~CSensorWitMotion();

        virtual void closePort(); // closes the port if open
        virtual bool detect();   // this detects & initializes the sensor
        virtual int send_data(char *send_buffer, int length);
        virtual int recv_data(char* recv_buffer, int length);
        virtual void ParseData(char chr);

        // note that CSensor defines a mean_xyz method that uses the read_xyz declared above -- you shouldn't need to override mean_xyz but that option is there
};

#endif

