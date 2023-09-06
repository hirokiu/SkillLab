#include "define.h"
//#include "csensor_usb_phidgets.h"
//#include "csensor_mac_usb_onavi.h"
//#include "csensor_linux_usb_onavi.h"
#include "csensor_witmotion.h"

#ifndef _WIN32
  #include <sys/time.h>   // for gettimeofday()
#endif

#include <fstream>
#include <iostream>
#include <iomanip>

CQCNShMem* sm = NULL;
std::ofstream writing_file;

// add your sensor class below, i.e. CSensorTest
int main(int argc, char** argv)
{
    const float RUN_SECONDS = 100.0f; // how many seconds to run -- max is 200 seconds (or bump up MAXI in define.h to RUN_SECONDS / DT )

    int iRetVal = 0, iErrCnt = 0;
    sm = new CQCNShMem();

    //CSensorUSBPhidgets sms;
    //CSensorMacUSBONavi sms;
    //CSensorLinuxUSBONavi sms;
    CSensorWitMotion sms;

    if (sms.detect()) {
       double tstart = dtime(), tend;
       // initialize timers
       sm->t0active = tstart; // use the function in boinc/lib
       sm->t0check = sm->t0active + sm->dt;

        char filename[128];
        sprintf(filename, "%s%s/csn.log", BASE_DIR, DATA_DIR);

        writing_file.open(filename, std::ios::out | std::ios::app);
        if (!writing_file.is_open()) {
            fprintf(stdout, "Couldn't open log file!\n");
            return false;
        }

       // assuming we're at 50Hz, run 500 times for 10 seconds of output, note array only holds 10,000 so don't go past that!
			 //sm->lOffset++;	//debug
       //for (sm->lOffset = 0; sm->lOffset < (int) (RUN_SECONDS / DT); sm->lOffset++) {	//debug
           while(true){
               if (!sms.mean_xyz(true)) iErrCnt++;   // pass in true for verbose output, false for silent
               #ifdef _DEBUG
                    fprintf(stdout, "___ X:%12f Y:%12f Z:%12f Active:%12f Check:%12f Sample:%2ld \n\n", sm->x1, sm->y1, sm->z1, sm->t0active, sm->t0check, sm->lSampleSize);
               #endif
               if( isAllTimeRecord ){
                   std::cout.setf(std::ios_base::fixed,std::ios_base::floatfield);
                   writing_file << std::setprecision(14) <<
                               sm->t0active << "," <<
                               sm->x1 << "," <<
                               sm->y1 << "," <<
                               sm->z1 << std::endl;
                           }

           }
           writing_file.close();

       tend = dtime();
       fprintf(stdout, "%f seconds of samples read from %f to %f in %f seconds real time -- error of %3.3f %c\n"
               "%d Timing Errors Encountered\n",
	  RUN_SECONDS, tstart, tend, tend - tstart, ((RUN_SECONDS - (tend - tstart)) / RUN_SECONDS) * 100.0f, '%', iErrCnt);
    }
    else {
       fprintf(stdout, "No sensor detected!\n");
       iRetVal = 1;
    }

    if (sm) {
        delete sm;
        sm = NULL;
    }

    return iRetVal;
}

// handle function from boinc/lib/util.C to get epoch time as a double
// return time of day (seconds since 1970) as a double
//
double dtime() {
#ifdef _WIN32
	LARGE_INTEGER time;
    FILETIME sysTime;
    double t;
    GetSystemTimeAsFileTime(&sysTime);
    time.LowPart = sysTime.dwLowDateTime;
    time.HighPart = sysTime.dwHighDateTime;  // Time is in 100 ns units
    t = (double)time.QuadPart;    // Convert to 1 s units
    t /= TEN_MILLION;                /* In seconds */
    t -= EPOCHFILETIME_SEC;     /* Offset to the Epoch time */
    return t;
#else
    struct timeval tv;
    gettimeofday(&tv, 0);
    return tv.tv_sec + (tv.tv_usec/1.e6);
#endif
}
