#include "global.h"
#include "stack.h"
#include "xstack.h"
#include "scheduler.h"
#include "bit_ops.h"
#include "timer0_isr.h"
#include "syscall.h"
#include "semaphore.h"
#include "events.h"
#include "seg_led.h"
#include "button.h"
#include "usbcom.h"
#include "rs485.h"
#include "random.h"

#define TIMESLICE_MS	1
#define T12RL		(65536 - MAIN_Fosc*TIMESLICE_MS/12/1000) 

/*
交互功能：
	导航上下左右 - 控制方向
	key3 - 发送落子信号
	key2 - 重开
	key1 - 打开网页，建立连接 / 关闭网页

通信规则：
0,1字节固定为aa 55
第2字节发送数据
	00 -- 打开网页
	01 -- 上
	02 -- 下
	03 -- 左
	04 -- 右
	05 -- 落子
	06 -- 重开
*/

unsigned char head[2] = {0xaa, 0x55};
unsigned char* buf;
unsigned char send_data[8];

void setSendData(unsigned char s0,unsigned char s1,unsigned char s2,unsigned char s3,unsigned char s4,unsigned char s5,unsigned char s6,unsigned char s7){
	send_data[0] = s0;
	send_data[1] = s1;
	send_data[2] = s2;
	send_data[3] = s3;
	send_data[4] = s4;
	send_data[5] = s5;
	send_data[6] = s6;
	send_data[7] = s7;
}


void myproc(u16 param) large reentrant{
	while(1){
		proc_wait_evts(EVT_BTN1_DN | EVT_BTN2_DN | EVT_BTN3_DN | EVT_NAV_L | EVT_NAV_R | EVT_NAV_U | EVT_NAV_D | EVT_NAV_PUSH | EVT_UART1_RECV | EVT_UART2_RECV);
		if((MY_EVENTS & EVT_BTN1_DN) == EVT_BTN1_DN){ // key1
			setSendData(0xaa,0x55,0x00,0x00,0x00,0x00,0x00,0x00);
			usbcom_write(send_data, 8);
		}
		else if((MY_EVENTS & EVT_BTN2_DN) == EVT_BTN2_DN){ // key2
			setSendData(0xaa,0x55,0x06,0x00,0x00,0x00,0x00,0x00);
			usbcom_write(send_data, 8);
		}
		else if((MY_EVENTS & EVT_BTN3_DN) == EVT_BTN3_DN){ // key3
			setSendData(0xaa,0x55,0x05,0x00,0x00,0x00,0x00,0x00);
			usbcom_write(send_data, 8);
		}
		else if((MY_EVENTS & EVT_NAV_L) == EVT_NAV_L){ // left
			setSendData(0xaa,0x55,0x03,0x00,0x00,0x00,0x00,0x00);
			usbcom_write(send_data, 8);
		}
		else if((MY_EVENTS & EVT_NAV_R) == EVT_NAV_R){ // right
			setSendData(0xaa,0x55,0x04,0x00,0x00,0x00,0x00,0x00);
			usbcom_write(send_data, 8);
		}
		else if((MY_EVENTS & EVT_NAV_U) == EVT_NAV_U){ // up
			setSendData(0xaa,0x55,0x01,0x00,0x00,0x00,0x00,0x00);
			usbcom_write(send_data, 8);
		}
		else if((MY_EVENTS & EVT_NAV_D) == EVT_NAV_D){ // down
			setSendData(0xaa,0x55,0x02,0x00,0x00,0x00,0x00,0x00);
			usbcom_write(send_data, 8);
		}
		else if((MY_EVENTS & EVT_NAV_PUSH) == EVT_NAV_PUSH){ // center
			setSendData(0xaa,0x55,0x07,0x00,0x00,0x00,0x00,0x00);
			usbcom_write(send_data, 8);
		}
		else if((MY_EVENTS & EVT_UART1_RECV) == EVT_UART1_RECV){ // uart1

		}
		else if((MY_EVENTS & EVT_UART2_RECV) == EVT_UART2_RECV){ // uart2
	
		}
	}
}

void timeproc(u16 param) large reentrant{
	u8 i = 0;
	while(1){

		if(i%10 == 0){}
		if(i%100 == 0){

		}
		if(i%1000 == 0){}
		proc_sleep(1);
		i++;
	}
}

main()
{
	//initialize kernel stack and xstack pointer
	SP = kernel_stack;
	setxbp(kernel_xstack + KERNEL_XSTACKSIZE);
	
	//set process stacks and swap stacks owner
	process_stack[0][PROCESS_STACKSIZE-1] = 0;
	process_stack[1][PROCESS_STACKSIZE-1] = 1;
	process_stack[2][PROCESS_STACKSIZE-1] = 2;
	process_stack[3][PROCESS_STACKSIZE-1] = 3;
	process_stack[4][PROCESS_STACKSIZE-1] = 4;
	process_stack_swap[0][PROCESS_STACKSIZE-1] = 5;
	process_stack_swap[1][PROCESS_STACKSIZE-1] = 6;
	process_stack_swap[2][PROCESS_STACKSIZE-1] = 7;
	
	//initialize LED pins
	P0M1 &= 0x00;
	P0M0 |= 0xff;
	P2M1 &= 0xf0;
	P2M0 |= 0x0f;
	//select LED, set all off
	P23 = 1;
	P0 = 0;

	//initialize buttons
	buttons_init();
	
	//initialize serial ports
	usbcom_init(9600);
	rs485_init(9600);

	setUartBuf(10, head, 2);
		
	//start process
	led_display_content = 0x00;
	start_process(myproc, 0, 0);
	start_process(timeproc, 1, 0);
		
		
	//initialize PCA2 interrupt (as syscall interrupt)
	//clear CCF2
	CCON &= ~0x04;
	//disable PCA2 module and set ECCF2
	CCAPM2 = 1;
	//low priority interrupt
	PPCA = 0;
	
	//start main timer
	TR0 = 0;														//stop timer
	TMOD &= 0xF0;												//timer mode, 16b autoreload
	AUXR &= 0x7F;												//12T mode
	TL0 = T12RL & 0xff;							//set reload value
	TH0 = (T12RL & 0xff00) >> 8;
	ET0 = EA = 1;												//set interrupt enable
	PT0 = 0;														//set priority to low
	TR0 = 1;														//start timer
	
	//spin
	while(1);
}