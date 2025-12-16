#ifndef __DS1302_H__
#define __DS1302_H__

typedef struct{
	unsigned char second;
	unsigned char minute;
	unsigned char hour;
	unsigned char day;
	unsigned char month;
	unsigned char year;
} Date;

/*
0-7为日期保存的地址，0 1 2 3 4 5 6保存秒 分 时 天 月 星期 年
7为写保护 0x00 - 可写 0x80 - 不可写

readDS1302和writeDS1302这两个函数是对芯片进行直接读写，没有考虑保护位。
getDate：获取日期
writeDate：写入日期
rRAM：从SRAM中读取数据（地址为0-31，对应31字节的SRAM，函数内部会转换成实际地址，不需要额外操作）
wRAM：写入数据（同样不需要额外操作）
*/

extern unsigned char readDS1302(unsigned char address); // 这两个函数是直接写/读，由于写保护的存在，直写在0x07不为0时不会生效
extern void writeDS1302(unsigned char address, unsigned char dat);
extern Date getDate();
extern void writeDate(Date d);
extern unsigned char rRAM(unsigned char address); // 读取RAM 地址范围：0-31
extern void wRAM(unsigned char address, unsigned char dat); // 写RAM 地址范围：0-31 写时需要先打开写保护


#endif
