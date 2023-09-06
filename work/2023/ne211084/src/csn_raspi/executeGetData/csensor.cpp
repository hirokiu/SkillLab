/*
 *  csensor.cpp
 *  qcn
 *
 *  Created by Carl Christensen on 08/11/2007.
 *  Copyright 2007 Stanford University.  All rights reserved.
 *
 * Implementation file for CSensor base classes
 * note it requires a reference to the sm shared memory datastructure (CQCNShMem)
 */

#include "csensor.h"
#include <math.h>
#include <cmath>
#include <complex>
//#include <except.h>

#include <pthread.h>

#include <fstream>
#include <iostream>
#include <iomanip>

using namespace std;

extern double dtime();

extern CQCNShMem* sm;
bool g_bStop = false;

// config for recording trigger
const float LTA_second = 10.0f;
const float STA_second = 5.0f;

int LTA_array_numbers = (int)(LTA_second / DT); //DT is defined in define.h
int STA_array_numbers = (int)(STA_second / DT); //DT is defined in define.h
int LTA_STA_diff = LTA_array_numbers - STA_array_numbers;

const float limitTimes = 1.5f;

const int triggerLimit = 1;
int triggerCount = 0;

const double recordTime = 60.0f; //second
double startRecordTime;

bool isEarthQuake = false;

// cmd name
char system_cmd[255];

CSensor::CSensor()
  :
    m_iType(SENSOR_NOTFOUND),
    m_port(-1),
    m_bSingleSampleDT(false),
    m_strSensor("")
{
}
/*
CSensor::CSensor(int d_id, double x_off, double y_off, double z_off)
  :
    m_iType(SENSOR_NOTFOUND),
    m_port(-1),
    m_bSingleSampleDT(false),
    m_strSensor("")
{
    device_id = d_id;
    x_offset = x_off;
    y_offset = y_off;
    z_offset = z_off;
}
*/
CSensor::~CSensor()
{
    if (m_port>-1) closePort();
}

bool CSensor::getSingleSampleDT()
{
   return m_bSingleSampleDT;
}

void CSensor::setSingleSampleDT(const bool bSingle)
{
   m_bSingleSampleDT = bSingle;
}

const char* CSensor::getSensorStr()
{
   return m_strSensor.c_str();
}

void CSensor::setSensorStr(const char* strIn)
{
    if (strIn)
       m_strSensor.assign(strIn);
    else
       m_strSensor.assign("");
}

void CSensor::setType(e_sensor esType)
{
   m_iType = esType;
}

void CSensor::setPort(const int iPort)
{
   m_port = iPort;
}

int CSensor::getPort()
{
   return m_port;
}

void CSensor::closePort()
{
    fprintf(stdout, "Closing port...\n");
}

const e_sensor CSensor::getTypeEnum()
{
   return m_iType;
}

const char* CSensor::getTypeStr()
{
   switch (m_iType) {
     case SENSOR_MAC_PPC_TYPE1:
        return "PPC Mac Type 1";
        break;
     case SENSOR_MAC_PPC_TYPE2:
        return "PPC Mac Type 2";
        break;
     case SENSOR_MAC_PPC_TYPE3:
        return "PPC Mac Type 3";
        break;
     case SENSOR_MAC_INTEL:
        return "Intel Mac";
        break;
     case SENSOR_WIN_THINKPAD:
        return "Lenovo Thinkpad";
        break;
     case SENSOR_WIN_HP:
        return "HP Laptop";
        break;
     case SENSOR_USB:
        return "JoyWarrior 24F8 USB";
        break;
     default:
        return "Not Found";
   }
}

// this is the heart of qcn -- it gets called 50-500 times a second!
inline bool CSensor::mean_xyz(const bool bVerbose)
{
/* This subroutine finds the mean amplitude for x,y, & z of the sudden motion
 * sensor in a window dt from time t0.
 */

	static long lLastSample = 10L;  // store last sample size, start at 10 so doesn't give less sleep below, but will if lastSample<3
	float x1,y1,z1;
	double dTimeDiff=0.0f;
	bool result = false;

	// set up pointers to array offset for ease in functions below
	float *px2, *py2, *pz2;
	double *pt2;

	if (g_bStop || !sm) throw EXCEPTION_SHUTDOWN;   // see if we're shutting down, if so throw an exception which gets caught in the sensor_thread

	px2 = (float*) &(sm->x0[sm->lOffset]);
	py2 = (float*) &(sm->y0[sm->lOffset]);
	pz2 = (float*) &(sm->z0[sm->lOffset]);
	pt2 = (double*) &(sm->t0[sm->lOffset]);
	sm->lSampleSize = 0L;

	*px2 = *py2 = *pz2 = *pt2 = 0.0f;  // zero sample averages

	// this will get executed at least once, then the time is checked to see if we have enough time left for more samples
	do {
		if (sm->lSampleSize < SAMPLE_SIZE) {  // note we only get a sample if sample size < 10
			x1 = y1 = z1 = 0.0f;
			result = read_xyz(x1, y1, z1);
			*px2 += x1;
			*py2 += y1;
			*pz2 += z1;
			sm->lSampleSize++; // only increment if not a single sample sensor
		}  // done sample size stuff

		// dt is in seconds, want to slice it into 10 (SAMPLING_FREQUENCY), put into microseconds, so multiply by 100000
		// using usleep saves all the FP math every millisecond

		// sleep for dt seconds, this is where the CPU time gets used up, for dt/10 6% CPU, for dt/1000 30% CPU!
		// note the use of the "lLastSample" -- if we are getting low sample rates i.e. due to an overworked computer,
		// let's drop the sleep time dramatically and hope it can "catch up"
		// usleep((long) lLastSample < 3 ? DT_MICROSECOND_SAMPLE/100 : DT_MICROSECOND_SAMPLE);

		usleep(DT_MICROSECOND_SAMPLE); // usually 2000, which is 2 ms or .002 seconds, 10 times finer than the .02 sec / 50 Hz sample rate
		sm->t0active = dtime(); // use the function in the util library (was used to set t0)
		dTimeDiff = sm->t0check - sm->t0active;  // t0check should be bigger than t0active by dt, when t0check = t0active we're done
	}
	while (dTimeDiff > 0.0f);

	//fprintf(stdout, "Sensor sampling info:  t0check=%f  t0active=%f  diff=%f  timeadj=%d  sample_size=%ld, dt=%f\n",
	//   sm->t0check, sm->t0active, dTimeDiff, sm->iNumReset, sm->lSampleSize, sm->dt);
	//fprintf(stdout, "sensorout,%f,%f,%f,%d,%ld,%f\n",
	//   sm->t0check, sm->t0active, dTimeDiff, sm->iNumReset, sm->lSampleSize, sm->dt);
	//fflush(stdout);

	lLastSample = sm->lSampleSize;

	// store values i.e. divide by sample size
	*px2 /= (double) sm->lSampleSize;
	*py2 /= (double) sm->lSampleSize;
	*pz2 /= (double) sm->lSampleSize;
	*pt2 = sm->t0active; // save the time into the array, this is the real clock time

    // To check isEarthQuake
    PreserveXYZ *tmp_xyz;
	tmp_xyz = new PreserveXYZ(px2, py2, pz2, pt2, &(sm->t0check), &(sm->lSampleSize), &(sm->lOffset));
    preserve_xyz.push_back(*tmp_xyz);
    delete tmp_xyz;

	if( preserve_xyz.size() > LTA_array_numbers ){
		preserve_xyz.erase(preserve_xyz.begin());
        preserve_xyz.shrink_to_fit();
	}

    // Everytime Record waves.
    if(isAllTimeRecord){
        // TODO:
		#ifdef _DEBUG
            fprintf(stdout, "X:%12f Y:%12f Z:%12f Active:%12f Check:%12f Sample:%2ld \n\n", *px2, *py2, *pz2, sm->t0active, sm->t0check, sm->lSampleSize);
        #endif
        sm->x1 = *px2;
        sm->y1 = *py2;
        sm->z1 = *pz2;
    }

	if(isEarthQuake) { // While a recordTime, couldn't check isEarthQuake
        // set triggered data
        PreserveXYZ *tmp_triggered;
        tmp_triggered = new PreserveXYZ(px2, py2, pz2, pt2, &(sm->t0check), &(sm->lSampleSize), &(sm->lOffset));
        triggered_xyz.push_back(*tmp_triggered);
        delete tmp_triggered;

		if(isQuitRecording()) {
            // output triggered data to file
            outputEarthQuake();

			//printf("Recording quits at %f\n", sm->t0check);
            std::deque<PreserveXYZ>().swap(triggered_xyz);
			isEarthQuake = false;
        }
	} else { // Only check isEarthQuake
        isEarthQuake = isStrikeEarthQuake();
	}

	// if active time is falling behind the checked (wall clock) time -- set equal, may have gone to sleep & woken up etc
	sm->t0check += sm->dt;	// t0check is the "ideal" time i.e. start time + the dt interval

	sm->fRealDT += fabs(sm->t0active - sm->t0check);

	if (fabs(dTimeDiff) > TIME_ERROR_SECONDS) { // if our times are different by a second, that's a big lag, so let's reset t0check to t0active
		if (bVerbose) {
			fprintf(stdout, "Timing error encountered t0check=%f  t0active=%f  diff=%f  timeadj=%d  sample_size=%ld, dt=%f, resetting...\n",
			sm->t0check, sm->t0active, dTimeDiff, sm->iNumReset, sm->lSampleSize, sm->dt);
		}

		#ifndef _DEBUG
			return false;   // if we're not debugging, this is a serious run-time problem, so reset time & counters & try again
		#endif
	}

	return true;
}

bool CSensor::isQuitRecording() {
	if((sm->t0check - startRecordTime) >= recordTime) {
		return true;
	}
	else return false;
}

bool CSensor::isStrikeEarthQuake()
{
	float LTA_x = 0.0f, STA_x = 0.0f;
	float LTA_y = 0.0f, STA_y = 0.0f;
	float LTA_z = 0.0f, STA_z = 0.0f;
	double LTA_x_average = 0.0f, STA_x_average = 0.0f;
	double LTA_y_average = 0.0f, STA_y_average = 0.0f;
	double LTA_z_average = 0.0f, STA_z_average = 0.0f;
    double LTA_x_offset = 0.0f;
    double LTA_y_offset = 0.0f;
    double LTA_z_offset = 0.0f;

	if(preserve_xyz.size() == LTA_array_numbers)
	{
		for(int i = preserve_xyz.size()-1; i >= 0; i--){
			LTA_x += preserve_xyz[i].tmp_x; // origin
			LTA_y += preserve_xyz[i].tmp_y; // origin
			LTA_z += preserve_xyz[i].tmp_z; // origin
        }
		LTA_x_offset = LTA_x / (double)LTA_array_numbers;
		LTA_y_offset = LTA_y / (double)LTA_array_numbers;
		LTA_z_offset = LTA_z / (double)LTA_array_numbers;

        LTA_x = 0.0f;
        LTA_y = 0.0f;
        LTA_z = 0.0f;
		for(int i = preserve_xyz.size()-1; i >= 0; i--)
		{
			LTA_x += fabs(preserve_xyz[i].tmp_x - LTA_x_offset);
			LTA_y += fabs(preserve_xyz[i].tmp_y - LTA_y_offset);
			LTA_z += fabs(preserve_xyz[i].tmp_z - LTA_z_offset);

			if(i == LTA_STA_diff){
				STA_x = LTA_x;
				STA_y = LTA_y;
				STA_z = LTA_z;
			}
		}

		LTA_x_average = LTA_x / (double)LTA_array_numbers;
		LTA_y_average = LTA_y / (double)LTA_array_numbers;
		LTA_z_average = LTA_z / (double)LTA_array_numbers;
		STA_x_average = STA_x / (double)STA_array_numbers;
		STA_y_average = STA_y / (double)STA_array_numbers;
		STA_z_average = STA_z / (double)STA_array_numbers;

		#ifdef _DEBUG
            if(fabs(LTA_x_average - STA_x_average) > 0.002) {
                fprintf(stdout, "X : %f %f %f %f %f\n\n", LTA_x, STA_x, LTA_x_average, STA_x_average, (LTA_x_average / STA_x_average));
            }
            if(fabs(LTA_y_average - STA_y_average) > 0.002) {
                fprintf(stdout, "Y : %f %f %f %f %f\n\n", LTA_y, STA_y, LTA_y_average, STA_y_average, (LTA_y_average / STA_y_average));
            }
            if(fabs(LTA_z_average - STA_z_average) > 0.002) {
                fprintf(stdout, "Z : %f %f %f %f %f\n\n", LTA_z, STA_z, LTA_z_average, STA_z_average, (LTA_z_average / STA_z_average));
            }
        #endif

        if( ((LTA_x_average == 0.0f) || (STA_x_average == 0.0f)) 
        	&& ((LTA_y_average == 0.0f) || (STA_y_average == 0.0f))
        	&& ((LTA_z_average == 0.0f) || (STA_z_average == 0.0f)) ) return false;

		if( (fabs(LTA_x_average * limitTimes) < fabs(STA_x_average))
			|| (fabs(LTA_y_average * limitTimes) < fabs(STA_y_average))
			|| (fabs(LTA_z_average * limitTimes) < fabs(STA_z_average)) ) {
			triggerCount++;

            #ifdef _DEBUG
				fprintf(stdout, "X: %f %f %f %f %f  - Trigger COUNT = %d\n\n", LTA_x, STA_x, LTA_x_average, STA_x_average, (LTA_x_average - STA_x_average), triggerCount);
				fprintf(stdout, "Y: %f %f %f %f %f  - Trigger COUNT = %d\n\n", LTA_y, STA_y, LTA_y_average, STA_y_average, (LTA_y_average - STA_y_average), triggerCount);
				fprintf(stdout, "Z: %f %f %f %f %f  - Trigger COUNT = %d\n\n", LTA_z, STA_z, LTA_z_average, STA_z_average, (LTA_z_average - STA_z_average), triggerCount);
            #endif

			if( triggerCount == triggerLimit ){
				triggerCount = 0;
				startRecordTime = preserve_xyz.back().tmp_id_t;
				//printf("Recording starts at %f\n", startRecordTime);	//for logging

                // make triggerd data
                triggered_xyz = preserve_xyz;

                // Trigger event execute.
                #ifdef _DEBUG
                    sprintf(system_cmd, "nohup %s/tools/propagation.sh %d %f %f %f %f &", BASE_DIR, device_id, startRecordTime, (fabs(STA_x_average)/fabs(LTA_x_average)), (fabs(STA_y_average)/fabs(LTA_z_average)), (fabs(STA_z_average)/fabs(LTA_z_average)) );
                    system(system_cmd);
                #endif

				return true;
			}
			else return false;
		} else {
			triggerCount = 0;
			return false;
		}
	}
	else return false;
}

bool CSensor::outputEarthQuake(){

    char filename[128];
    sprintf(filename, "%s%s/%03d_%f%s", BASE_DIR, TRIG_DIR, device_id, startRecordTime, FILE_EXTENSION);

	std::ofstream ofs( filename );
    if (!ofs.is_open()) {
        return false;
    }

    cout.setf(ios_base::fixed,ios_base::floatfield);
    for(int i = 0; i < triggered_xyz.size(); i++){
        ofs << setprecision(20) <<
		triggered_xyz[i].tmp_t << "," <<
                triggered_xyz[i].tmp_x << "," <<
                triggered_xyz[i].tmp_y << "," <<
                triggered_xyz[i].tmp_z << std::endl;
    }
    ofs.close();

    return true;
}
