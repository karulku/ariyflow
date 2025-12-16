#ifndef __UART2_H__
#define __UART2_H__

extern void uart2Init(unsigned long baudrate);
extern void uart2Send(unsigned char* content, unsigned char num);
extern void setUart2Buf(unsigned char* buf, unsigned char buf_num);

#endif