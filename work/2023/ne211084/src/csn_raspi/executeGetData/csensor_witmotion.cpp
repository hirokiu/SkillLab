/*
 *  csensor_witmotion.cpp
 *  qcn
 *
 *  Created by Hiroki UEMATSU on 03/12/2021.
 *  Copyright 2007 Stanford University.  All rights reserved.
 *
 * Implementation file for a new QCN sensor derived from the CSensor class
 *
 * Ideally you will just need to edit & implement this class to add a new sensor to QCN (i.e. via csensor_test.h & .cpp)
 */

#include "define.h"
#include "csensor_witmotion.h"

#include <glob.h>

#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<unistd.h>
#include<assert.h>
#include<termios.h>
#include<string.h>
#include<sys/time.h>
#include<time.h>
#include<sys/types.h>
#include<errno.h>

const int g_ciLen = 44;  // ##XXYYZZC
extern CQCNShMem* sm;

#define N_SPEED 115200 //115200 for JY61 ,9600 for others
#define N_BITS 8
#define N_EVENT 'N'
#define N_STOP 1

CSensorWitMotion::CSensorWitMotion()
  : CSensor()
{  // any initializations for public/private member vars here
}

CSensorWitMotion::~CSensorWitMotion()
{  // at the very least close the port if open!
  closePort();
}

void CSensorWitMotion::closePort()
{
  if (getPort() > -1) {
    fprintf(stdout, "Closing WitMotion sensor port...\n");

    // what ever port closure logic is required can go here...

    fprintf(stdout, "Port closed!\n");
    fflush(stdout);
    setPort(); // sets to -1 i.e. inactive/notfound
  }

    assert(m_fd);
    close(m_fd);
}

bool CSensorWitMotion::detect()
{
   // this is where you try to detect & open the sensor
   // it's pretty obvious -- if detected/opened return true, if not return false
   // if detected you'll want to set the port & type (see csensor.h & define.h for types)
   // we'll just call it SENSOR_TEST for now and set the port to the enum value
   // (the m_port member var can be used to set an int number to a specific port, if necessary)

    // use glob to match names, if count is > 0, we found a match
    glob_t gt;
    memset(&gt, 0x00, sizeof(glob_t));
    if (glob(STR_LINUX_USB_WITMOTION01, GLOB_NOCHECK, NULL, &gt) || !gt.gl_pathc) {  // either glob failed or no match
        // device string failed, but try the new string onavi (really Exar USB driver) may be using
        //if (glob(STR_USB_ONAVI02, GLOB_NOCHECK, NULL, &gt) || !gt.gl_matchc) {  // either glob failed or no match
            globfree(&gt);
            return false;
        //}
    }

    char* strDevice = new char[_MAX_PATH];
    memset(strDevice, 0x00, sizeof(char) * _MAX_PATH);
    strncpy(strDevice, gt.gl_pathv[0], _MAX_PATH);
    globfree(&gt); // can get rid of gt now

    //fd = open(pathname, O_RDWR|O_NOCTTY);
    m_fd = open(strDevice, O_RDWR | O_NOCTTY);

    if (-1 == m_fd)
    {
#ifdef _DEBUG
        fprintf(stderr, "Cannot create WitMotion fd\n");
#endif
        perror("Can't Open Serial Port");
        return false;
    }
    else
        printf("open %s success!\n", strDevice);
        delete [] strDevice; // don't need strDevice after this call
        strDevice = NULL;
    if(isatty(STDIN_FILENO)==0)
        printf("standard input is not a terminal device\n");
    else
        printf("isatty success!\n");
    //return m_fd;

    // setup basic modem I/O
    struct termios newtio,oldtio;
    if  ( tcgetattr(m_fd,&oldtio)  !=  0) {
        perror("SetupSerial 1");
        printf("tcgetattr( m_fd,&oldtio) -> %d\n",tcgetattr(m_fd,&oldtio));
        return false;
    }
    bzero( &newtio, sizeof( newtio ) );
    newtio.c_cflag  |=  CLOCAL | CREAD;
    newtio.c_cflag &= ~CSIZE;

    switch( N_BITS )
    {
        case 7:
            newtio.c_cflag |= CS7;
            break;
         case 8:
            newtio.c_cflag |= CS8;
            break;
    }
    switch( N_EVENT )
    {
        case 'o':
        case 'O':
            newtio.c_cflag |= PARENB;
            newtio.c_cflag |= PARODD;
            newtio.c_iflag |= (INPCK | ISTRIP);
            break;
        case 'e':
        case 'E':
            newtio.c_iflag |= (INPCK | ISTRIP);
            newtio.c_cflag |= PARENB;
            newtio.c_cflag &= ~PARODD;
            break;
        case 'n':
        case 'N':
            newtio.c_cflag &= ~PARENB;
            break;
        default:
            break;
    }

     /*设置波特率*/

switch( N_SPEED )
    {
        case 2400:
            cfsetispeed(&newtio, B2400);
            cfsetospeed(&newtio, B2400);
            break;
        case 4800:
            cfsetispeed(&newtio, B4800);
            cfsetospeed(&newtio, B4800);
            break;
        case 9600:
            cfsetispeed(&newtio, B9600);
            cfsetospeed(&newtio, B9600);
            break;
        case 115200:
            cfsetispeed(&newtio, B115200);
            cfsetospeed(&newtio, B115200);
            break;
        /* Not Found
        case 460800:
            cfsetispeed(&newtio, B460800);
            cfsetospeed(&newtio, B460800);
            break;
        */
        default:
            cfsetispeed(&newtio, B9600);
            cfsetospeed(&newtio, B9600);
            break;
    }
    if( N_STOP == 1 )
         newtio.c_cflag &=  ~CSTOPB;
    else if ( N_STOP == 2 )
        newtio.c_cflag |=  CSTOPB;
        newtio.c_cc[VTIME]  = 0;
        newtio.c_cc[VMIN] = 0;
    tcflush(m_fd,TCIFLUSH);

    if((tcsetattr(m_fd,TCSANOW,&newtio))!=0)
    {
        perror("com set error");
        return -1;
    }
    printf("set done!\n");

    setType(SENSOR_USB);
    setPort((int) getTypeEnum());

    fprintf(stdout, "WitMotion sensor %s detected.\n",getTypeStr());
    bzero(r_buf,1024);
    return true;

}

// now all you need to do is define how to read x/y/z values from the sensor
// for now just return random numbers
bool CSensorWitMotion::read_xyz(float& x1, float& y1, float& z1)
{
    // return true if read OK, false if error
    // the real timing work, i.e. the 50Hz sampling etc is done in mean_xyz in CSensor -- you shouldn't need (or want!) to edit that

    static float x0 = 0.0f, y0 = 0.0f, z0 = 0.0f; // keep last values
    bool bRet = true;

    QCN_BYTE bytesIn[g_ciLen+1], cs;  // note pad bytesIn with null \0
    int x = 0, y = 0, z = 0;
    int iCS = 0;
    static int iRead = 0;
        x1 = x0; y1 = y0; z1 = z0;  // use last good values

    const char cWrite = '*';

    // first check for valid port
    if (getPort() < 0) {
        return false;
    }


    if( (ret = recv_data(r_buf,g_ciLen)) != -1 )
    {
        for (int i=0;i<ret;i++)
        {
            ParseData(r_buf[i]);
        }
        x1 = a[0]; y1 = a[1]; z1 = a[2];  // current values
        x0 = x1; y0 = y1; z0 = z1;  // preserve values
        bRet = true;
    }
    else {
        fprintf(stderr, "%f: WitMotion Error in read_xyz() - write(*) returned %d -- errno = %d : %s\n", sm->t0active, ret, errno, strerror(errno));
        bRet = false;
    }

    // QCN will try and sample up to 10 times every .02 seconds by default (up to 500Hz of samples which is software downsampled to 50Hz)
    // You can also set a boolean flag if your hardware does the sub-sampling and we just need to read at 50Hz
    // If your hardware supports it, just add the following line to the detect() logic above:
    //    setSingleSampleDT(true);

    // try to also scale your output (xyz) to be a +/- 2g range

    // also if you only have a 2-axis accelerometer don't forget to set z1 to 0.0f!

    /*
    bool bRetVal = true;
    try {
        x1 = (float) ((rand() % 100) - 50) / 25.0f;    // NB this will give random floats between -2.0 & 2.0
        y1 = (float) ((rand() % 100) - 50) / 25.0f;    // NB this will give random floats between -2.0 & 2.0
        z1 = (float) ((rand() % 100) - 50) / 25.0f;    // NB this will give random floats between -2.0 & 2.0
    }
    catch(...) {
        bRetVal = false;
    }
    */

    //usleep(10000);  // uncommenting this line will force timing errors since it sleeps a second every read!
    return bRet;

}



int CSensorWitMotion::send_data(char *send_buffer,int length)
{
	length=write(m_fd,send_buffer,length*sizeof(unsigned char));
	return length;
}
int CSensorWitMotion::recv_data(char* recv_buffer,int length)
{
	length=read(m_fd,recv_buffer,length);
	return length;
}

void CSensorWitMotion::ParseData(char chr)
{
        static char chrBuf[100];
        static unsigned char chrCnt=0;
        signed short sData[4];
        unsigned char i;
        char cTemp=0;
        time_t now;
        chrBuf[chrCnt++]=chr;
        if (chrCnt<11) return;
        for (i=0;i<10;i++) cTemp+=chrBuf[i];
        if ((chrBuf[0]!=0x55)||((chrBuf[1]&0x50)!=0x50)||(cTemp!=chrBuf[10])) {printf("Error:%x %x\r\n",chrBuf[0],chrBuf[1]);memcpy(&chrBuf[0],&chrBuf[1],10);chrCnt--;return;}

        memcpy(&sData[0],&chrBuf[2],8);
        switch(chrBuf[1])
        {
                case 0x51:
                    for (i=0;i<3;i++) a[i] = (float)sData[i]/32768.0*16.0;
                    //time(&now);
                    //printf("\r\nT:%s a:%6.16f %6.16f %6.16f ",asctime(localtime(&now)),a[0],a[1],a[2]);
                    break;
                case 0x52:
                    for (i=0;i<3;i++) w[i] = (float)sData[i]/32768.0*2000.0;
                    //printf("w:%7.3f %7.3f %7.3f ",w[0],w[1],w[2]);
                    break;
                case 0x53:
                    for (i=0;i<3;i++) Angle[i] = (float)sData[i]/32768.0*180.0;
                    //printf("A:%7.3f %7.3f %7.3f ",Angle[0],Angle[1],Angle[2]);
                    break;
                case 0x54:
                    for (i=0;i<3;i++) h[i] = (float)sData[i];
                    //printf("h:%4.0f %4.0f %4.0f ",h[0],h[1],h[2]);
                    break;
        }
        chrCnt=0;
}