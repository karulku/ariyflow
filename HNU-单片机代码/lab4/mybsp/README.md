原先lab1已实现模块：

    display, key, adc, sys, uart1, stepmotor

相比原先新增模块：

    uart2, AT24C02, fm, DS1302(时钟与31字节SRAM读写均可)
  
芯片数据手册：

    https://wwawf.lanzouu.com/b0139dw6cd
  
    密码:hz06

使用样例：

    https://wwawf.lanzouu.com/iQ0sZ3dukl9c

不要问我没有regx52.h怎么办，自己解决。STM32就是cube配置，非常简单。

小提示：fm收音机使用的RDA5807FP芯片，进行IIC通信时不需要传入寄存器地址，具体参照datasheet。
