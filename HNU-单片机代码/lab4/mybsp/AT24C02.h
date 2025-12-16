#ifndef __AT24C02_H__
#define __AT24C02_h__

/*
main中调用Init即可。
AT24C02有256字节的非易失存储，对应地址0x00-0xff
  rAT：读取某个地址的数据
  wAT：向某个地址写数据
*/

extern void ATInit();
extern unsigned char rAT(unsigned char addr);
extern void wAT(unsigned char addr, unsigned char val);


#endif
