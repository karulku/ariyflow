#ifndef __UART2_H__
#define __UART2_H__

/*
和串口1类似。
uart2没有做包头检测，只需要传入接收数据的缓冲区
uart2使用定时器2做波特率产生器，不同于uart1使用定时器1，所以两个串口的波特率可以不同；
这里的波特率采用了lab2学长的计算方法，和uart1的查表不同，支持的波特率没有进行测试，但应该比uart1更多
*/

extern void uart2Init(unsigned long baudrate);
extern void uart2Send(unsigned char* content, unsigned char num);
extern void setUart2Buf(unsigned char* buf, unsigned char buf_num);


#endif
