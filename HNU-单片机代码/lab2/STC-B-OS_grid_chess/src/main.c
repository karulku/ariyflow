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
点格棋

交互功能：
导航左右键 - 更新位选
导航上下键 - 更新段选
key3 - 确定位置

编码规则：
共8个字节
第0,1字节为 aa 55
第2字节为功能位
00 -- 更新棋盘
	此时为棋盘更新
	aa 55 00 xa xb xx xx xx xa为位选 xb为段选
01 -- 此时为结束，由某一个单片机发送数据后，另一个单片机返回数据
	aa 55 01 xa xb xx xx xx xa为本机地址 xb为分数
*/

unsigned char head[2] = {0xaa, 0x55};
unsigned char* buf;
xdata unsigned char local_addr = 0x01; // 本机地址
xdata unsigned char target_addr = 0x00; // 目标机地址 
xdata unsigned char chess_board[8] = {0,0,0,0,0,0,0,0}; // 棋盘
xdata unsigned char play_turn = 0; // 当前正在下棋的地址
xdata unsigned char d_cur=0,w_cur=0; // 当前的游标位置（段选）和数码管位置（位选）
xdata unsigned char spark = 0; // 闪烁的标志位，每1s更新一次
xdata unsigned char send_data[8]; // 要发送的数据
xdata unsigned char score = 0x00, target_score=0; // 本机分数和目标机分数
xdata unsigned char is_end = 0; // 判断是否结束

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

void update_w_cur(unsigned char dir){
	if(dir == 1){
		w_cur = (w_cur+1)%8;
		while(chess_board[w_cur] == 0x7f)w_cur = (w_cur+1)%8;
	}
	else if(dir == 0){
		if(w_cur == 0)w_cur = 7;
		else w_cur--;

		while(chess_board[w_cur] == 0x7f){
			if(w_cur == 0)w_cur = 7;
			else w_cur--;
		}
	}
}

void update_d_cur(unsigned char dir){
	if(dir == 1){
		if(d_cur == 0)d_cur = 6;
		else d_cur--;

		while((chess_board[w_cur]&(1<<d_cur)) == (1<<d_cur)){
			if(d_cur == 0)d_cur = 6;
			else d_cur--;
		}
	}
	else if(dir == 0){
		d_cur = (d_cur+1)%7;
		while((chess_board[w_cur]&(1<<d_cur)) == (1<<d_cur))d_cur = (d_cur+1)%7;
	}
}

unsigned char check_board_is_full(){ // 检查棋盘是否占满
	u8 i = 0;
	for(i=0;i<8;i++){
		if(chess_board[i]!=0x7f)return 0;
	}
	return 1;
}

unsigned char check_state(unsigned char w_cur, unsigned char d_cur){
	if(d_cur == 0 || d_cur == 1 || d_cur == 5){
		return ((chess_board[w_cur] & 0x63) == 0x63);
	}
	else if(d_cur == 2 || d_cur == 3 || d_cur == 4){
		return ((chess_board[w_cur] & 0x5c) == 0x5c);
	}
	else if(d_cur == 6){
		return ((chess_board[w_cur] & 0x63) == 0x63)+((chess_board[w_cur] & 0x5c) == 0x5c);
	}
	else return 0;
}

void myproc(u16 param) large reentrant{
	while(1){
		proc_wait_evts(EVT_BTN1_DN | EVT_BTN2_DN | EVT_BTN3_DN | EVT_NAV_L | EVT_NAV_R | EVT_NAV_U | EVT_NAV_D | EVT_NAV_PUSH | EVT_UART1_RECV | EVT_UART2_RECV);
		if((MY_EVENTS & EVT_UART2_RECV) == EVT_UART2_RECV){ // uart2
			if(rs485_buf[0] == 0xaa && rs485_buf[1] == 0x55){
				if(rs485_buf[2] == 0x00){ // 更新棋盘
					chess_board[rs485_buf[3]] |= (1<<rs485_buf[4]);
					
					// 如果没有形成闭环，进入我的回合
					if(check_state(rs485_buf[3], rs485_buf[4]) == 0){
						play_turn = local_addr;
						if(chess_board[w_cur] == 0x7f) update_w_cur(1);
						if((chess_board[w_cur] & (1<<d_cur)) == (1<<d_cur)) update_d_cur(1);
					}
				}
				else if(rs485_buf[2] == 0x01){ // 结束
					target_score = rs485_buf[4];
					is_end = 1;
				}
			}
		}

		// 仅在当前是本机回合的时候，导航按键和key3才有效
		if(play_turn == local_addr){
			if((MY_EVENTS & EVT_NAV_L) == EVT_NAV_L){ // left
				update_w_cur(0);
				if((chess_board[w_cur]&(1<<d_cur)) == (1<<d_cur)) update_d_cur(1);
			}
			else if((MY_EVENTS & EVT_NAV_R) == EVT_NAV_R){ // right
				update_w_cur(1);
				if((chess_board[w_cur]&(1<<d_cur)) == (1<<d_cur)) update_d_cur(1);
			}
			else if((MY_EVENTS & EVT_NAV_U) == EVT_NAV_U){ // up
				update_d_cur(1);
			}
			else if((MY_EVENTS & EVT_NAV_D) == EVT_NAV_D){ // down
				update_d_cur(0);
			}
			else if((MY_EVENTS & EVT_BTN3_DN) == EVT_BTN3_DN){ // key3
				chess_board[w_cur] |= (1<<d_cur);

				if(check_board_is_full()){ // 棋盘已满，进入结算
					if(d_cur == 6)score+=2; // 更新后棋盘满，一定有一个形成闭环
					else score++;
					
					setSendData(0xaa,0x55,0x01,local_addr,score,0,0,0);
					rs485_write(send_data, 8);

					is_end = 1;
				}
				else{ // 棋盘未满，更新显示，继续游戏
					if(check_state(w_cur, d_cur)){ // 如果形成闭环，继续游戏
						score=score+check_state(w_cur, d_cur);
					}
					else{
						play_turn = target_addr; // 没有闭环，更换回合
					}

					setSendData(0xaa,0x55,0x00,w_cur,d_cur,0x00,0x00,0x00);
					rs485_write(send_data, 8);

					if(chess_board[w_cur] == 0x7f) update_w_cur(1); // 棋盘更新后更新显示位置
					if((chess_board[w_cur] & (1<<d_cur)) == (1<<d_cur))update_d_cur(1);
				}
			}
			else if((MY_EVENTS & EVT_NAV_PUSH) == EVT_NAV_PUSH){ // center

			}
		}
	}
}

void timeproc(u16 param) large reentrant{
	u8 i = 0;
	while(1){

		if(i%10 == 0){}
		if(i%100 == 0){
			if(is_end == 0){
				if(play_turn == local_addr){ // 当前是本机回合
					setSegDir(chess_board[0],chess_board[1],chess_board[2],chess_board[3],chess_board[4],chess_board[5],chess_board[6],chess_board[7]);
					if(spark == 1){
						setSegAdd(w_cur, d_cur);
					}
					led_display_content = score;
				}
				else{ // 当前不是本机回合
					setSegDir(chess_board[0],chess_board[1],chess_board[2],chess_board[3],chess_board[4],chess_board[5],chess_board[6],chess_board[7]);
				}
			}
			else if(is_end == 1){
				target_score = 16 - score;
				setSeg(46,46,score/10,score%10,46,46,target_score/10,target_score%10);
				led_display_content = 0x00;
			}

		}
		if(i%1000 == 0){
			spark = (1 - spark);
		}
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

	setUartBuf(8, head, 2);
		
	//start process
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