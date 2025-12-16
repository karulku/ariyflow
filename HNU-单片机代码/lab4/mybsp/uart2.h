#ifndef __UART2_H__
#define __UART2_H__

/*
和串口1类似。
uart2没有做包头检测，只需要传入接收数据的缓冲区
uart2使用定时器2做波特率产生器，不同于uart1使用定时器1，所以两个串口的波特率可以不同；
波特率只有9600测试正常，其他没有测试（因为我做实验用的是9600）
支持的波特率：
  1200
  2400
  4800
  9600
  19200
  38400
  57600
  115200
*/

extern void uart2Init(unsigned long baudrate);
extern void uart2Send(unsigned char* content, unsigned char num);
extern void setUart2Buf(unsigned char* buf, unsigned char buf_num);


#endif

