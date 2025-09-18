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
#include"uart2.h"
#include"M24C02.h"
#include"intrins.h"
#include"IR.h"
#include"DS1302.h"


void Delay(unsigned char xms)		//@11.0592MHz
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


// 上位机程序

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
unsigned char led_vector;

unsigned char uart_head[2] = {0x10,0x29}; // 串口检测数据包头
unsigned char receive_buf[8]; // 串口接收缓冲区
unsigned char seg[8]; // 数码管向量
unsigned char mode = 0; // 模式选择
unsigned char NVM_addr = 0x01; // 非易失存储地址
unsigned char ir_buf[8]; // 红外缓冲区
unsigned char dis_addr; // 目标下位机地址
unsigned char set_state; // 设置时间的状态，低三位表示时分秒
unsigned char uart_buf[8]; // 串口缓冲区（串口2）
unsigned char h,m,s; // 暂时保存设置的超时时间
struct_DS1302_RTC ds_time;

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

void showSeg(){
	Seg7Print(seg[0],seg[1],seg[2],seg[3],seg[4],seg[5],seg[6],seg[7]);
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

void irSet(uchar a, uchar b, uchar c, uchar d, uchar e, uchar f, uchar g, uchar h){
	ir_buf[0] = a;
	ir_buf[1] = b;
	ir_buf[2] = c;
	ir_buf[3] = d;
	ir_buf[4] = e;
	ir_buf[5] = f;
	ir_buf[6] = g;
	ir_buf[7] = h;
}

void my100mSCallback(){
	LedPrint(mode+1);
	if(mode == 0){
		showSeg();
	}
	else if(mode == 1){
		unsigned char addr,hour,minute,second;
		addr = M24C02_Read(NVM_addr);
		hour = M24C02_Read(NVM_addr+1);
		minute = M24C02_Read(NVM_addr+2);
		second = M24C02_Read(NVM_addr+3);
		Seg7Print(addr/10,addr%10,hour/10,hour%10,minute/10,minute%10,second/10,second%10);
	}
	else if(mode == 2){
		segSet(46,46,46,46,46,46,dis_addr/10,dis_addr%10);
		showSeg();
	}
	else if(mode == 3){
		segSet(h/10,h%10,48,m/10,m%10,48,s/10,s%10);
		if(set_state == 0x01)seg[7] += 16;
		else if(set_state == 0x02)seg[4] += 16;
		else if(set_state == 0x04)seg[1] += 16;
		showSeg();
	}
}

void myKeyCallback(){
	unsigned char key;
	key = GetKeyAct(enumKey2);
	if(key == enumKeyPress){
		mode = (mode+1)%4;
		if(mode == 0){
			segSet(0,0,0,0,0,0,0,0);
			showSeg();
		}
		if(mode == 3){
			segSet(0,0,0,0,0,0,0,0);
		}
	}
	
	if(mode == 2){
		key = GetKeyAct(enumKey1);
		if(key == enumKeyPress){
			irSet(0x10,0x29,0xff,0x02,dis_addr, 0x00,0x00,0x00);
			IrPrint(ir_buf, 8);
		}
	}
}

void myADCCallback(){
	unsigned char key;
	if(mode == 1){
		
		key = GetAdcNavAct(enumAdcNavKeyUp);
		if(key == enumKeyPress){
			if(NVM_addr<0xfd){
				NVM_addr = NVM_addr+4;
			}
		}
		
		key = GetAdcNavAct(enumAdcNavKeyDown);
		if(key == enumKeyPress){
			if(NVM_addr>0x01){
				NVM_addr = NVM_addr-4;
			}
		}
	}
	if(mode == 2){ // 发送关闭指令的模式
		key = GetAdcNavAct(enumAdcNavKeyUp);
		if(key == enumKeyPress){
			if(dis_addr<99){
				dis_addr = dis_addr+1;
			}
		}
		key = GetAdcNavAct(enumAdcNavKeyDown);
		if(key == enumKeyPress){
			if(dis_addr>0){
				dis_addr = dis_addr-1;
			}
		}
	}
	
	if(mode == 3){ // 设置超时时间的模式
		key = GetAdcNavAct(enumAdcNavKeyCenter);
		if(key == enumKeyPress){
			if(set_state == 0x00)set_state = 0x04;
			else{
				set_state = 0x00;
			}
		}
		key = GetAdcNavAct(enumAdcNavKeyLeft);
		if(key == enumKeyPress){
			if(set_state!=0x04)set_state = (set_state<<1);
		}
		key = GetAdcNavAct(enumAdcNavKeyRight);
		if(key == enumKeyPress){
			if(set_state!=0x01)set_state = (set_state>>1);
		}
		key = GetAdcNavAct(enumAdcNavKey3);
		if(key == enumKeyPress){
			uartbufSet(0x10,0x29,0x02,0x00,h,m,s,0x00);
			Uart2Print(uart_buf, 8);
		}
		key = GetAdcNavAct(enumAdcNavKeyUp);
		if(key == enumKeyPress){ // 按上键+1
			if(set_state==0x01 && s<59)s+=1;
			else if(set_state==0x02 && m<59)m+=1;
			else if(set_state==0x04 && h<59)h+=1;
		}
		key = GetAdcNavAct(enumAdcNavKeyDown);
		if(key == enumKeyPress){
			if(set_state==0x01&&s>0)s-=1;
			else if(set_state==0x02&&m>0)m-=1;
			else if(set_state==0x04&&h>0)h-=1;
		}
	}
	
}

void myUart1Callback(){
	
}

void myUart2Callback(){
	unsigned char now_addr;
	if(mode == 0){
		if(receive_buf[2] == 0xff){
			if(receive_buf[3] == 0x00){ // 收到时间，在数码管上显示并保存到非易失存储中,数码管依次显示：从机地址，时，分，秒
				segSet(receive_buf[4]/10,receive_buf[4]%10,receive_buf[5]/10,receive_buf[5]%10,receive_buf[6]/10,receive_buf[6]%10,receive_buf[7]/10,receive_buf[7]%10);
				now_addr = M24C02_Read(0x00);
				M24C02_Write(now_addr,receive_buf[4]);
				Delay(10);
				M24C02_Write(now_addr+1,receive_buf[5]);
				Delay(10);
				M24C02_Write(now_addr+2,receive_buf[6]);
				Delay(10);
				M24C02_Write(now_addr+3,receive_buf[7]);
				Delay(10);
				if(now_addr<=0xf8)
					M24C02_Write(0x00,now_addr+4);
				else{
					M24C02_Write(0x00, 0x01);
				}
			}
			else if(receive_buf[3] == 0x01){ // 收到超时信号
				SetBeep(1200, 100);
				segSet(48,48,48,receive_buf[4]/10,receive_buf[4]%10,48,48,48);
			}
		}
	}
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
	IrInit(NEC_R05d);
	DS1302Init(ds_time);
	Uart1Init(9600);
	Uart2Init(9600, Uart2Usedfor485);
	SetUart1Rxd(receive_buf, 8, uart_head, 2);
	SetUart2Rxd(receive_buf, 8, uart_head, 2);
	
	led_vector = 0xaa;
	Seg7Print(46,46,46,46,46,46,46,46);
	LedPrint(0);
	h = 0;
	m = 0;
	s = 0;

	SetEventCallBack(enumEventSys100mS,my100mSCallback);
	SetEventCallBack(enumEventKey,myKeyCallback);
	SetEventCallBack(enumEventXADC,myADCCallback);
	SetEventCallBack(enumEventUart1Rxd, myUart1Callback);
	SetEventCallBack(enumEventUart2Rxd,myUart2Callback);
	
	while(1){
		MySTC_OS();
	}
}