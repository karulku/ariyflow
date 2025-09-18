#include<STC15F2K60S2.H>
#include"sys.h"
#include"displayer.h"
#include"Beep.h"
#include"key.h"
#include"ADC.h"
#include"uart1.h"
#include"uart2.h"
#include"IR.h"
#include"DS1302.h"
#include"FM_Radio.h"
#include"intrins.h"
// 下位机程序
/*
编码规则：
	第0,1字节为数据包头，第2个字节标识功能
	
	第0,1字节固定为10 29
	第2字节为功能字节：
		00 -- 刷视频助手，下位机与PC双向通信
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
					01 -- 打开b站（下位机 -> PC）  (10 29 00 xx 01 xx xx xx) 触发打开b站事件
					
					02 -- 关闭串口（该功能在新版中已弃用）  (10 29 00 xx 02 xx xx xx)
								关闭单片机和电脑的连接，慎用，关闭后只能从PC端的程序打开串口
								由于关闭串口单片机无法操作程序，所以程序打开后默认会打开一次串口
								关闭后单片机无法与计算机通信，所以无法使用单片机再次打开串口
								
					03 -- 时间信号（PC -> 下位机） 发送时间，此时第5，6，7字节表示时，分，秒
								该信号在刷视频结束（关闭PC程序时，不受超时信号影响）触发，数码管显示时-分-秒，上位机也会同步显示
					
					04 -- 超时信号（PC -> 下位机） 由PC发送来的超时信号，下位机收到该信号后报警，并将信号传递给下位机
								超时时数码管会显示 00-00-00
		ff -- 上下位机通信
			下位机向上位机发送指令:
				
	
	
交互功能：
	数码管6,7 -- 显示要发送的指令
	key1 -- 发送前置指令打开b站
	key3 -- 发送数据
	导航上键 -- 指令+1
	导航下键 -- 指令-1
	导航中键 -- 清0
	导航左键 -- 关闭串口
	
	注意后面对于模式的定义有两种，一种是单片机内部的模式，该模式由mode定义，另一种是单片机串口通信的模式，该模式由buf缓冲区的第2个字节定义
*/

const unsigned char code DECODE_TABLE[] = { 
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
    0x3e, 0x1c, 0x7e, 0x64, 0x6e, 0x5a, 0x00, 0xFF,  // 40-47
//  U(40) V(41) W(42) X(43) Y(44) Z(45) None  ALL
		0x40
};

#define uchar unsigned char

code unsigned long SysClock=11059200;
unsigned char local_addr = 0x01; // 这是本机地址，不可修改！！！
unsigned char uart_buf[8],receive_buf[8]; // 串口发送和接收的缓冲区
unsigned char xdata seg[8] = {46,46,46,46,46,46,46,46}; // 数码管显示向量
unsigned char code uart_head[2] = {0x10,0x29}; // 包头
unsigned char ir_buf[8]; // 红外缓冲区
unsigned char adc_buf[8]; // 传送adc数据的专用缓冲区
unsigned char mode = 0; // 全局模式
unsigned char clk_mode = 0; // 时钟内部的模式
struct_ADC adc; // adc值
struct_DS1302_RTC clk = {0x00,0x00,0x00,0x00,0x00,0x00,0x00}; // 时钟信息
struct_FMRadio xdata fm = {918,5,0,0,0}; // 收音机信息
unsigned char xdata fm_state = 0x00; // 保存fm的状态，第0位标识频率是否可调整，第1位标识音量是否可调整
unsigned char xdata receive2_buf[8]; // 串口2的接收缓冲区

void showSeg(){
	Seg7Print(seg[0],seg[1],seg[2],seg[3],seg[4],seg[5],seg[6],seg[7]);
}

void uartbufSet(uchar a, uchar b, uchar c, uchar d, uchar e, uchar f, uchar g, uchar h){
	uart_buf[0]=a;
	uart_buf[1]=b;
	uart_buf[2]=c;
	uart_buf[3]=d;
	uart_buf[4]=e;
	uart_buf[5]=f;
	uart_buf[6]=g;
	uart_buf[7]=h;
}

void adcbufSet(uchar a, uchar b, uchar c, uchar d, uchar e, uchar f, uchar g, uchar h){
	adc_buf[0]=a;
	adc_buf[1]=b;
	adc_buf[2]=c;
	adc_buf[3]=d;
	adc_buf[4]=e;
	adc_buf[5]=f;
	adc_buf[6]=g;
	adc_buf[7]=h;
}

void segSet(uchar a, uchar b, uchar c, uchar d, uchar e, uchar f, uchar g, uchar h){
	seg[0] = a;
	seg[1] = b;
	seg[2] = c;
	seg[3] = d;
	seg[4] = e;
	seg[5] = f;
	seg[6] = g;
	seg[7] = h;
}

void myDelay(unsigned char xms)		//@11.0592MHz
{
	while(xms--){
		unsigned char i, j;

		_nop_();
		_nop_();
		_nop_();
		i = 11;
		j = 190;
		do
		{
			while (--j);
		} while (--i);
	}
}

void my100mSCallback(){
	LedPrint(mode+1);
	if(mode == 0){ // 默认模式
		if(uart_buf[2] == 0x00){ // 视频助手模式
			segSet(46,46,46,46,46,46,(uart_buf[3]&0xf0)>>4, (uart_buf[3]&0x0f));
			// 测试代码，后续删除
			// segSet((uart_buf[4]&0xf0)>>4, (uart_buf[4]&0x0f),(uart_buf[5]&0xf0)>>4, (uart_buf[5]&0x0f),(uart_buf[6]&0xf0)>>4, (uart_buf[6]&0x0f),(uart_buf[7]&0xf0)>>4, (uart_buf[7]&0x0f));
		}
		else if(uart_buf[2] == 0xff){ // 双机通信模式
			if(receive_buf[3] == 0x00){
				segSet(receive_buf[5]/10,receive_buf[5]%10,48,receive_buf[6]/10,receive_buf[6]%10,48,receive_buf[7]/10,receive_buf[7]%10);
			}
			else if(receive_buf[3] == 0x01){
				uartbufSet(0x10,0x29,0xff,0x01,0x00,0x00,0x00,0x00);
				Uart1Print(uart_buf, 8);
			}
		}
	}
	
	if(mode == 1){ // 如果是时钟模式
		clk = RTC_Read();
		if(clk_mode == 0){
			segSet(clk.hour>>4,clk.hour&0x0f,48,clk.minute>>4,clk.minute&0x0f,48,clk.second>>4,clk.second&0x0f);
			showSeg();
		}
		else if(clk_mode == 1){
			segSet(clk.year>>4,clk.year&0x0f,48,clk.month>>4,clk.month&0x0f,48,clk.day>>4,clk.day&0x0f);
			showSeg();
		}
		else if(clk_mode == 2){
			segSet(48,48,48,48,48,48,clk.week>>4,clk.week&0x0f);
			showSeg();
		}
	}
	
	if(mode == 2){ // 收音机模式
		segSet(48,fm.frequency/100,fm.frequency/10%10+16,fm.frequency%10,48,48,fm.volume/10,fm.volume%10);
		showSeg();
	}
	
	showSeg();
}

void myKeyCallback(){
	unsigned char key;
	
	key = GetKeyAct(enumKey2);
	if(key == enumKeyPress){
		mode = (mode+1)%3;
		
		// 这里放mode切换后需要执行的操作
		if(mode == 1){
			clk_mode = 0;
		}
		
		if(mode == 0){
			// 注意这里，在发送完毕之后，需要把uart_buf[2]切换回0x00，否则会出现问题（shit山代码）
			uart_buf[2] = 0x00;
			fm_state = 0x00;
		}
	}
	
	if(mode == 0){
		if(uart_buf[2] == 0x00){
			key = GetKeyAct(enumKey1);
			if(key == enumKeyPress){
				uartbufSet(0x10,0x29,0x00,0x00,0x01,0x00,0x00,0x00);
				Uart1Print(uart_buf, 8);
			}
		}
	}

	if(mode == 1){ // 时钟模式下
		key = GetKeyAct(enumKey1); // 按下key1键切换显示模式
		if(key == enumKeyPress){
			clk_mode = (clk_mode+1)%3;
		}
	}
	
	if(mode == 2){ // 收音机模式
		key = GetKeyAct(enumKey1); // key1时控制音量
		if(key == enumKeyPress){
			if((fm_state&0x02) != 0x02)fm_state = (fm_state ^ 0x01); // 如果正在调整频率，指令无效
			if((fm_state&0x01) == 0x01){ // 按下后状态为调整音量，触发一次提示音
				SetBeep(800, 20);
			}
			else{ // 按下后为调整完成，触发另一个提示音
				uartbufSet(0x10,0x29,0x01,0x01,(fm.frequency>>8),(fm.frequency&0x00ff),fm.volume,0x00);
				Uart1Print(uart_buf, 8);
				SetBeep(600,20);
			}
		}
	}
}

void myADCCallback(){
	unsigned char key;
	if(mode == 0){ // mode 0：控制串口发送
		if(uart_buf[2] == 0x00){
			key = GetAdcNavAct(enumAdcNavKey3);
			if(key == enumKeyPress){
				uartbufSet(0x10,0x29,0x00,uart_buf[3],0x00,0x00,0x00,0x00);
				Uart1Print(uart_buf, 8);
			}
			key = GetAdcNavAct(enumAdcNavKeyUp);
			if(key == enumKeyPress){
				uart_buf[3]++;
			}
			key = GetAdcNavAct(enumAdcNavKeyDown);
			if(key == enumKeyPress){
				uart_buf[3]--;
			}
			key = GetAdcNavAct(enumAdcNavKeyCenter);
			if(key == enumKeyPress){
				uart_buf[3] = 0x00;
			}
		}
	}
	
	if(mode == 2){ // 收音机模式下，如果fm_state对应位为1，调整频率或音量
		key = GetAdcNavAct(enumAdcNavKey3);
		if(key == enumKeyPress){
			if((fm_state&0x01) != 0x01)fm_state = (fm_state ^ 0x02); // 如果正在调整音量，指令无效
			if((fm_state&0x02) == 0x02){
				SetBeep(800,20);
			}
			else{
				uartbufSet(0x10,0x29,0x01,0x01,(fm.frequency>>8),(fm.frequency&0x00ff),fm.volume,0x00);
				Uart1Print(uart_buf, 8);
				SetBeep(600,20);
			}
		}
		
		key = GetAdcNavAct(enumAdcNavKeyUp);
		if(key == enumKeyPress){
			if((fm_state&0x01) == 0x01){
				if(fm.volume<15)fm.volume = fm.volume+1;
			}
			else if((fm_state&0x02) == 0x02){
				if(fm.frequency<1080)fm.frequency = fm.frequency+1;
			}
		}
		
		key = GetAdcNavAct(enumAdcNavKeyDown);
		if(key == enumKeyPress){
			if((fm_state&0x01)==0x01){
				if(fm.volume>0)fm.volume = fm.volume-1;
			}
			else if((fm_state&0x02)==0x02){
				if(fm.frequency>887)fm.frequency = fm.frequency-1;
			}
		}
		SetFMRadio(fm);
	}

}

void myUart1Callback(){
	char state;
	uart_buf[2] = receive_buf[2]; // 模式切换
	LedPrint(uart_buf[2]);

	
	if(receive_buf[2] == 0x00){ // 刷视频模式，接收从PC传来的超时信号和时间信号
		if(receive_buf[4] == 0x03){ // 收到结束信号，传递刷视频的时间
			// 这里处理传递逻辑
			uartbufSet(0x10,0x29,0xff,0x00,local_addr,receive_buf[5],receive_buf[6],receive_buf[7]);
			Uart2Print(uart_buf, 8);
		}
		else if(receive_buf[4] == 0x04){ // 超时信号，报警提醒，并将信号传递给上位机
			SetBeep(1200,100);
			uartbufSet(0x10,0x29,0xff,0x01,local_addr,0x00,0x00,0x00);
			Uart2Print(uart_buf, 8);
			state = GetUart2TxStatus();
			if(state == enumUart1TxFree){
				uart_buf[2] = 0x00;
			}
		}
	}
	
	if(receive_buf[2] == 0x01){ // 辅助功能，目前只提供同步时钟
		if(receive_buf[3] == 0x01){ // PC传递时钟信息
			if(receive_buf[4] == 0x00){ // 年月日
				clk = RTC_Read();
				clk.year = ((receive_buf[5]/10)<<4)+(receive_buf[5]%10);
				clk.month = ((receive_buf[6]/10)<<4)+(receive_buf[6]%10);
				clk.day = ((receive_buf[7]/10)<<4)+(receive_buf[7]%10);
				RTC_Write(clk);
			}
			else if(receive_buf[4] == 0x01){ // 时分秒
				clk = RTC_Read();
				clk.hour = ((receive_buf[5]/10)<<4)+(receive_buf[5]%10);
				clk.minute = ((receive_buf[6]/10)<<4)+(receive_buf[6]%10);
				clk.second = ((receive_buf[7]/10)<<4)+(receive_buf[7]%10);
				RTC_Write(clk);
			}
			else if(receive_buf[4] == 0x02){ // 星期
				clk = RTC_Read();
				clk.week = ((receive_buf[5]/10)<<4)+(receive_buf[5]%10+1);
				RTC_Write(clk);
			}
		}
	}

}

void myUart2Callback(){
	if(receive2_buf[2] == 0x02){ // 上位机直接和PC通信，直接发到串口1
		Uart1Print(receive2_buf, 8);
	}
}

void myIRCallback(){
	if((ir_buf[0] == 0x10) && (ir_buf[1] == 0x29)){
		if((ir_buf[2] == 0xff) && (ir_buf[4] == local_addr)){
			if(ir_buf[3] == 0x02){ // 强制停机指令
				uartbufSet(0x10,0x29,0x00,0xfe,0x00,0x00,0x00,0x00);
				Uart1Print(uart_buf, 8); // 需要添加停机逻辑
			}
		}
	}
}

unsigned char xdata adc_turn = 0;
void my1SCallback(){
	// 这里发送adc值
	
	adc = GetADC();
	if(adc_turn){
		adcbufSet(0x10,0x29,0x01,0x00,0x00,(adc.Rop>>8),(adc.Rop&0x00ff),0x00);
		Uart1Print(adc_buf, 8);
	}
	else{
		adcbufSet(0x10,0x29,0x01,0x00,0x01,(adc.Rt>>8),(adc.Rt&0x00ff),0x00);
		Uart1Print(adc_buf, 8);
	}
	adc_turn = (1 - adc_turn);
	
}

void main(){
	MySTC_Init();
	DisplayerInit();
	BeepInit();
	KeyInit();
	AdcInit(ADCexpEXT);
	IrInit(NEC_R05d);
	Uart1Init(9600);
	Uart2Init(9600, Uart2Usedfor485);
	DS1302Init(clk);
	FMRadioInit(fm);
	
	SetUart1Rxd(receive_buf, 8, uart_head, 2);
	SetUart2Rxd(receive2_buf, 8, uart_head, 2);
	SetIrRxd(ir_buf, 8);
	Seg7Print(46,46,46,46,46,46,46,46);
	LedPrint(0);
	
	SetEventCallBack(enumEventSys100mS,my100mSCallback);
	SetEventCallBack(enumEventKey,myKeyCallback);
	SetEventCallBack(enumEventXADC,myADCCallback);
	SetEventCallBack(enumEventUart1Rxd, myUart1Callback);
	SetEventCallBack(enumEventUart2Rxd, myUart2Callback);
	SetEventCallBack(enumEventIrRxd, myIRCallback);
	SetEventCallBack(enumEventSys1S, my1SCallback);
	while(1){
		MySTC_OS();
	}
}