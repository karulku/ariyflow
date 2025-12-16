#ifndef __FM_H__
#define __FM_H__

/*
main中调用Init函数
打开收音机或者修改音量，频率时，调用update_params函数
关闭时调用stopFM函数
*/

extern void fmInit();
extern void update_params(unsigned int fre, unsigned char vol);
extern void stopFM();


#endif
