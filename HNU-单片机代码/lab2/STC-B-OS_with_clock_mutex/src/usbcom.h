#ifndef _USBCOM_H_
#define _USBCOM_H_

#include "global.h"
#include "scheduler.h"
#include "bit_ops.h"

extern XDATA u8 usbcom_buf[64];
extern XDATA u8 usbcom_rxcnt;
extern XDATA u32 usbcom_timeout;
extern XDATA u8 usbcom_evtstate;

void usbcom_init(u32 baudrate); //VCALL_UL

#define usbcom_write(buf,len) NOINT_ATOMIC(__usbcom_write(buf,len);)
void __usbcom_write(u8* buf, u8 len) small;

void setUartBuf(char buf_size, char* head, char head_size); // buf_size只能是0-64, head_size必须小于等于buf_size
void* readBuf();

#endif