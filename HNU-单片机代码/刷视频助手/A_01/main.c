#include<STC15F2K60S2.H>
#include"sys.h"
#include"displayer.h"
#include"Beep.h"
#include"hall.H"
#include"key.h"
#include"ADC.h"
#include"music.h"
#include"stepmotor.h"
#include"Vib.h"
#include"uart1.h"

/*
00 -- 刷视频助手
	编码规则：
		第0,1字节为数据包头，第2个字节为00 标识功能
		
		第3个字节为指令
			00 -- 刷新页面
			ff -- 退出视频（如果打开了视频，没有打开视频会直接退出）
			01 -- 点开第1个视频 02 -- 点开第2个视频 03 -- 点开第2个视频
			04 -- 点开第4个视频 05 -- 点开第5个视频 06 -- 点开第6个视频
			fe -- 直接退出，不管是否打开视频
			
			比如：10 29 00 00 00 xx xx xx 表示刷新页面
		
		第4个字节为前置指令
			这条指令为00时正常处理第3个字节的指令
			这条指令不为00时会触发前置指令操作：
				01 -- 打开b站  (10 29 00 xx 01 xx xx xx) 触发打开b站事件
				02 -- 关闭串口  (10 29 00 xx 02 xx xx xx)
					关闭单片机和电脑的连接，慎用，关闭后只能从PC端的程序打开串口
					由于关闭串口单片机无法操作程序，所以程序打开后默认会打开一次串口
					关闭后单片机无法与计算机通信，所以无法使用单片机再次打开串口
		
		
	交互功能：
		数码管6,7 -- 显示要发送的指令
		key1 -- 发送前置指令打开b站
		key3 -- 发送数据
		导航上键 -- 指令+1
		导航下键 -- 指令-1
		导航中键 -- 清0
		导航左键 -- 关闭串口
*/

unsigned char code DECODE_TABLE[] = { 
    0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, // 0-7
//  0(0)  1(1)  2(2)  3(3)  4(4)  5(5)  6(6)  7(7)
    0x7F, 0x6F, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71, // 8-15
//  8(8)  9(9)  a(10) b(11) c(12) d(13) e(14) f(15)
    0xBF, 0x86, 0xDB, 0xcF, 0xE6, 0xED, 0xFD, 0x87, // 16-23
//  0.(16)1.(17)2.(18)3.(19)4.(20)5.(21)6.(22)7.(23)
    0xFF, 0xEF, 0x3d, 0x76, 0x0f, 0x0E, 0x75, 0x38, // 24-31
//  8.(24)9.(25)G(26) H(27) I(28) J(29) K(30) L(31)
    0x37, 0x54, 0x5c, 0x73, 0x67, 0x31, 0x49, 0x78, // 32-39
//  M(32) N(33) O(34) P(35) Q(36) R(37) S(38) T(39)
    0x3e, 0x1c, 0x7e, 0x64, 0x6e, 0x5a, 0x00, 0xFF  // 40-47
//  U(40) V(41) W(42) X(43) Y(44) Z(45) None  ALL
};

code unsigned long SysClock=11059200;
unsigned char led_vector;
unsigned char cnt;
unsigned char uart_buf[8],head[2]={0x10,0x29},receive_buf[8];

void my100mSCallback(){
	Seg7Print(46,46,46,46,46,46,cnt>>4,cnt&(0x0f));
}

void myKeyCallback(){
	unsigned char key;
	key = GetKeyAct(enumKey1); // key1键按下后发送打开b站指令
	if(key == enumKeyPress){
		uart_buf[0]=0x10,uart_buf[1]=0x29,uart_buf[2]=0x00,uart_buf[4]=0x01;
		Uart1Print(uart_buf,8);
	}
}

void myADCCallback(){
	unsigned char key;
	key = GetAdcNavAct(enumAdcNavKey3); // key3键按下，发送数据cnt
	if(key == enumKeyPress){
		uart_buf[0] = 0x10,uart_buf[1] = 0x29,uart_buf[2] = 0x00,uart_buf[3] = cnt,uart_buf[4]=0x00;
		Uart1Print(uart_buf,8);
	}
	key = GetAdcNavAct(enumAdcNavKeyUp); // 上键cnt+1
	if(key == enumKeyPress){
		cnt++;
	}
	key = GetAdcNavAct(enumAdcNavKeyDown); // 下键cnt-1
	if(key == enumKeyPress){
		cnt--;
	}
	key = GetAdcNavAct(enumAdcNavKeyCenter); // 中心键重置cnt
	if(key == enumKeyPress){
		cnt = 0;
	}
	key = GetAdcNavAct(enumAdcNavKeyLeft); // 左键发送关闭串口指令
	if(key == enumKeyPress){
		uart_buf[0]=0x10,uart_buf[1]=0x29,uart_buf[2]=0x00,uart_buf[4]=0x02;
		Uart1Print(uart_buf,8);
	}
	
}

void myUart1Callback(){
	
}

void main(){
	MySTC_Init();
	DisplayerInit();
	BeepInit();
	HallInit();
	KeyInit();
	AdcInit(ADCexpEXT);
	MusicPlayerInit();
	StepMotorInit();
	VibInit();
	Seg7Print(46,46,46,46,46,46,46,46);
	LedPrint(0);
	Uart1Init(9600);
	SetUart1Rxd(receive_buf,8,head,2);
	SetEventCallBack(enumEventSys100mS,my100mSCallback);
	
	SetEventCallBack(enumEventKey,myKeyCallback);
	SetEventCallBack(enumEventUart1Rxd,myUart1Callback);
	SetEventCallBack(enumEventXADC,myADCCallback);
	
	while(1){
		MySTC_OS();
	}
}