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
#include "mutex.h"

#define TIMESLICE_MS	1
#define T12RL		(65536 - MAIN_Fosc*TIMESLICE_MS/12/1000) 


void testproc(u16 param) large reentrant
{
	while(1)
	{
		if((timer0_cnt>>5) & BIT(param))
		{
			SETBIT(led_display_content, param);
		}
		else
		{
			CLEARBIT(led_display_content, param);
		}
	}
}

void testproc2(u16 param) large reentrant
{
	while(1)
	{
		proc_sleep(param);
		led_display_content = ~led_display_content;
	}
}

void testproc3(u16 param) large reentrant
{
	while(1)
	{
		proc_sleep(param);
		led_display_content ^= 0x0f;
	}
}

void testproc4() large reentrant
{
	while(1)
	{
		proc_sleep(500);
		sem_post(0);
		led_display_content |= 0x80;
		sem_wait(0);
		led_display_content &= ~0x80;
	}
}

void testproc5() large reentrant
{
	sem_init(0,0);
	while(1)
	{
		sem_wait(0);
		led_display_content |= 0x40;
		proc_sleep(500);
		sem_post(0);
		led_display_content &= ~0x40;
	}
}

void testproc6(u16 param) large reentrant
{
	while(1)
	{
		proc_wait_evts(EVT_BTN1_DN);
		seg_set_str("HELLO   ");
		usbcom_write("hello \0",0);
		proc_wait_evts(EVT_NAV_R);
		seg_set_str("WORLD   ");
		usbcom_write("world\r\n\0",0);
		proc_wait_evts(EVT_UART1_RECV);
		seg_set_str(usbcom_buf);
	}
}

void testproc7(u16 param) large reentrant
{
	while(1)
	{
		proc_wait_evts(EVT_UART2_RECV | EVT_BTN1_DN);
		if(MY_EVENTS & EVT_BTN1_DN)
		{
			*((u32 *)rs485_buf) = rand32();
			rs485_write(rs485_buf, 4);
			seg_set_number(*((u32 *)rs485_buf));
		}
		else
		{
			seg_set_number(*((u32 *)rs485_buf));
		}
	}
}


DSTime t;
unsigned char buf[7];
unsigned char time_state = 0;
void myproc(u16 param) large reentrant{
	while(1){
		proc_wait_evts(EVT_BTN1_DN | EVT_BTN2_DN | EVT_BTN3_DN | EVT_NAV_L | EVT_NAV_R | EVT_NAV_U | EVT_NAV_D | EVT_NAV_PUSH | EVT_UART1_RECV | EVT_UART2_RECV);
		if((MY_EVENTS & EVT_BTN1_DN) == EVT_BTN1_DN){ // key1
			t.minute = 2;
			t.second = 15;
			setSysTime(t);
		}
		else if((MY_EVENTS & EVT_BTN2_DN) == EVT_BTN2_DN){ // key2
			time_state = (1 - time_state);
		}
		else if((MY_EVENTS & EVT_BTN3_DN) == EVT_BTN3_DN){ // key3
			led_display_content ^= 0x04;
		}
		else if((MY_EVENTS & EVT_NAV_L) == EVT_NAV_L){ // left
			led_display_content ^= 0x10;
		}
		else if((MY_EVENTS & EVT_NAV_R) == EVT_NAV_R){ // right
			led_display_content ^= 0x20;
		}
		else if((MY_EVENTS & EVT_NAV_U) == EVT_NAV_U){ // up
			led_display_content ^= 0x40;
		}
		else if((MY_EVENTS & EVT_NAV_D) == EVT_NAV_D){ // down
			led_display_content ^= 0x80;
		}
		else if((MY_EVENTS & EVT_NAV_PUSH) == EVT_NAV_PUSH){ // center
			led_display_content ^= 0x08;
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
		if(i%1000 == 0){
			t = getSysTime();
			buf[0] = t.year;
			buf[1] = t.month;
			buf[2] = t.day;
			buf[3] = t.hour;
			buf[4] = t.minute;
			buf[5] = t.second;
			if(time_state == 0) setSeg(t.hour/10,t.hour%10,48,t.minute/10,t.minute%10,48,t.second/10,t.second%10);
			else if(time_state == 1) setSeg(t.year/10, t.year%10, 48, t.month/10, t.month%10, 48, t.day/10, t.day%10);
			led_display_content = ds1302_readbyte(DS1302_WP);
		}
		proc_sleep(1);
		i++;
	}
}

unsigned long cnt = 0;
unsigned long cnt1=0,cnt2=0;
lock_t mut1,mut2;
void lockproc1(u16 param){
	u16 i = 0;

	while(1){
		while(i < 1000){

			// 信号量
			sem_wait(0);
			cnt = cnt+1;
			sem_post(0);

			// 锁
			// lock(&mut1);
			// cnt = cnt + 1;
			// unlock(&mut1);

			// 开关中断
			// DISABLE_INTERRUPTS();
			// ++cnt;
			// proc_sleep(5);
			// ENABLE_INTERRUPTS();

			// ++cnt;

			setSegl4(cnt/1000,cnt/100%10,cnt/10%10,cnt%10);
			i = i + 1;
		}

		setSegl4(cnt/1000,cnt/100%10,cnt/10%10,cnt%10);
	}
}

void lockproc2(u16 param){
	u16 i = 0;
	sem_init(0, 1);

	while(1){
		while(i < 1000){

			// 信号量
			sem_wait(0);
			cnt = cnt+1;
			sem_post(0);

			// 锁
			// lock(&mut1);
			// cnt = cnt + 1;
			// unlock(&mut1);

			// 开关中断
			// DISABLE_INTERRUPTS();
			// ++cnt;
			// proc_sleep(5);
			// ENABLE_INTERRUPTS();

			// ++cnt;

			setSegr4(cnt/1000,cnt/100%10,cnt/10%10,cnt%10);
			i = i + 1;
		}

		setSegr4(cnt/1000,cnt/100%10,cnt/10%10,cnt%10);
	}
}

void lockTimeProc(u16 param){
	while(1){
		ENABLE_INTERRUPTS();
		setSeg(0,0,0,0,cnt/1000,cnt/100%10,cnt/10%10,cnt%10);
		proc_sleep(100);
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
		
	//start process
	led_display_content = 0x00;

	// 演示时钟的代码
	// start_process(myproc, 0, 0);
	// start_process(timeproc, 1, 0);

	// 测试信号量
	// start_process(testproc4, 2, 0);
	// start_process(testproc5, 3, 0);

	lock_init(&mut1);
	lock_init(&mut2);
	
	
	// start_process(lockproc2, 1, 0);
	// start_process(lockproc1, 2, 0);

	start_process(timeproc, 3, 0);
	start_process(myproc, 4, 0);
		
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