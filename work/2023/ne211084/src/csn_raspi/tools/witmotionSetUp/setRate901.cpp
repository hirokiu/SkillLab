/*=========================================================
WitMotion setRate
BWT901CLのサンプリング周波数を変更するためのプログラム

Raspberry Pi以外で実行する場合、センサーが接続されているttyがどこか、
/dev/ttyXXX を確認し、プログラムを修正すること

環境に合わせて、以下のコマンドでコンパイル
gcc -o setRatexxx setRate.cpp

コマンド実行後、センサーの再起動が必要
USBケーブルを抜いて、電源オフしてから電源オン
=========================================================*/
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

static int ret;
static int fd;

#define BAUD 115200 //115200 for JY61 ,9600 for others

int uart_open(int fd,const char *pathname)
{
    fd = open(pathname, O_RDWR|O_NOCTTY);
    if (-1 == fd)
    {
        perror("Can't Open Serial Port");
		return(-1);
	}
    else
		printf("open %s success!\n",pathname);
    if(isatty(STDIN_FILENO)==0)
		printf("standard input is not a terminal device\n");
    else
		printf("isatty success!\n");
    return fd;
}

int uart_set(int fd,int nSpeed, int nBits, char nEvent, int nStop)
{
     struct termios newtio,oldtio;
     if  ( tcgetattr( fd,&oldtio)  !=  0) {
      perror("SetupSerial 1");
	  printf("tcgetattr( fd,&oldtio) -> %d\n",tcgetattr( fd,&oldtio));
      return -1;
     }
     bzero( &newtio, sizeof( newtio ) );
     newtio.c_cflag  |=  CLOCAL | CREAD;
     newtio.c_cflag &= ~CSIZE;
     switch( nBits )
     {
     case 7:
      newtio.c_cflag |= CS7;
      break;
     case 8:
      newtio.c_cflag |= CS8;
      break;
     }
     switch( nEvent )
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

switch( nSpeed )
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
     case 460800:
      cfsetispeed(&newtio, B460800);
      cfsetospeed(&newtio, B460800);
      break;
     default:
      cfsetispeed(&newtio, B9600);
      cfsetospeed(&newtio, B9600);
     break;
     }
     if( nStop == 1 )
      newtio.c_cflag &=  ~CSTOPB;
     else if ( nStop == 2 )
      newtio.c_cflag |=  CSTOPB;
     newtio.c_cc[VTIME]  = 0;
     newtio.c_cc[VMIN] = 0;
     tcflush(fd,TCIFLUSH);

if((tcsetattr(fd,TCSANOW,&newtio))!=0)
     {
      perror("com set error");
      return -1;
     }
     printf("set done!\n");
     return 0;
}

int uart_close(int fd)
{
    assert(fd);
    close(fd);

    return 0;
}
int send_data(int  fd, char *send_buffer,int length)
{
	length=write(fd,send_buffer,length*sizeof(unsigned char));
	return length;
}
int recv_data(int fd, char* recv_buffer,int length)
{
	length=read(fd,recv_buffer,length);
	return length;
}
float a[3],w[3],Angle[3],h[3];
void ParseData(char chr)
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
                    time(&now);
                    printf("\r\nT:%s a:%6.16f %6.16f %6.16f ",asctime(localtime(&now)),a[0],a[1],a[2]);
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

int main(void)
{
    char r_buf[1024];
    bzero(r_buf,1024);

    fd = uart_open(fd,"/dev/ttyUSB0");/*串口号/dev/ttySn,USB口号/dev/ttyUSBn */
    //fd = uart_open(fd,"/dev/ttyAMA0");/*串口号/dev/ttySn,USB口号/dev/ttyUSBn */
    if(fd == -1)
    {
        fprintf(stderr,"uart_open error\n");
        exit(EXIT_FAILURE);
    }

    if(uart_set(fd,BAUD,8,'N',1) == -1)
    {
        fprintf(stderr,"uart set failed!\n");
        exit(EXIT_FAILURE);
    }

    // set Return Rage
/*
    char change_rate_100[] = "0xFF0xAA0x030x090x00"; // 100
    char change_rate_50[] = "0xFF0xAA0x030x080x00"; // 50
    char change_rate_10[] = "0xFF0xAA0x030x060x00"; // 10
*/
    char _unlock[5];
    _unlock[0] = 0xFF;
    _unlock[1] = 0xAA;
    _unlock[2] = 0x69;
    _unlock[3] = 0x88;
    _unlock[4] = 0xB5;

    // 設定したいサンプリング周波数に応じて変更
    char change_rate[5];
    change_rate[0]= 0xFF;
    change_rate[1]= 0xAA;
    change_rate[2]= 0x03;
    //change_rate[3]= 0x06; //10Hz
    //change_rate[3]= 0x08; //50Hz
    change_rate[3]= 0x09; //100Hz
    change_rate[4]= 0x00;

    char save_conf[5];
    save_conf[0] = 0xFF;
    save_conf[1] = 0xAA;
    save_conf[2] = 0x00;
    save_conf[3] = 0;
    save_conf[4] = 0x00;

    ret = send_data(fd, _unlock, 5);
    printf("set UNLOCK: %d , command:%s \n", ret, _unlock);
    usleep(100000);

    ret = send_data(fd, change_rate, 5);
    printf("set Return Rate: %d , command:%s \n", ret, change_rate);
    usleep(100000);

    send_data(fd, save_conf, 5);
    printf("SAVE Configuration: %d, command:%s \n", ret, save_conf);
    usleep(100000);

    ret = uart_close(fd);
    if(ret == -1)
    {
        fprintf(stderr,"uart_close error\n");
        exit(EXIT_FAILURE);
    }

    printf("EXIT...! \n");
    exit(EXIT_SUCCESS);
}
