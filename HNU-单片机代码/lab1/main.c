#include <sys.h>
#include <sm.h>
#include <display.h>
#include <adc.h>
#include <key.h>
#include <uart1.h>
/*
lab 1 第一版

交互功能：
数码管显示三个步进电机的速度，从右向左为sm0,sm1,sm2,可以显示速度，加速度，方向信息
	注意在加速度页面，由于加速度允许负数（-10，10），但是数码管无法同时显示三个负数，
	所以显示的内容是真实值+10后的结果，也就是（0，20）
LED由于需要模拟两个步进电机，无法显示其他信息

key1键 -- 所有电机加速
key2键 -- 所有电机减速
此时加速度固定为5

key3键 -- 切换当前显示的内容；初始显示速度，按下key3后在 速度-加速度-转动方向 之间轮换

导航键可以设置三个步进电机的速度，加速度或者方向
导航中键 -- 打开或关闭设置模式，设置模式下对应的位置会有小数点
导航上键 -- 速度+1
导航下键 -- 速度-1
导航左键 -- 小数点左移
导航右键 -- 小数点右移

通信规则：
0,1字节固定为aa 55
第2字节标识电机
	00 - sm0
		3,4,5字节标识数据
			3 - 速度
			4 - 加速度
			5 - 转动方向
			6,7 - 剩余步数
	01 - sm1
		同sm0
	02 - sm2
		同sm0
	03 - 传输数据 此时传输温度和光照的数据
	aa 55 03 xa xb xc xd 00 # xa xb为温度adc值，xc xd为光照adc值
*/

unsigned char speed[3] = {5,5,5}; // 保存数码管要显示的速度
char acc[3] = {0,0,0}; // 初始加速度
unsigned char dir[3] = {0,0,0}; // 初始方向
unsigned char is_setting = 0; // 是否处于设置模式
unsigned char set_pos = 0x00; // 设置的位置 00 - sm0; 01 - sm1; 02 - sm2;
unsigned char show_state = 0x00; // 当前的显示内容 00 - 速度; 01 - 加速度; 02 - 转动方向;
unsigned char key;
char acc_state = 0; // 保存key1和key2的状态
ADC adc;
xdata unsigned char seg_buf[8]; // 保存数码管将要显示的信息
xdata unsigned char i = 0;
xdata unsigned char buf[8],rcv[8],head[2] = {0xaa,0x55};

extern xdata unsigned char _speeds[3]; // 由于加速度的原因，需要获取真实速度，但是懒得写api了
extern xdata char _acc[3];
extern xdata unsigned char _dirs[3];
extern xdata unsigned int _steps[3];

void ssb(char s0,char s1,char s2,char s3,char s4,char s5,char s6,char s7){
	seg_buf[0] = s0;
	seg_buf[1] = s1;
	seg_buf[2] = s2;
	seg_buf[3] = s3;
	seg_buf[4] = s4;
	seg_buf[5] = s5;
	seg_buf[6] = s6;
	seg_buf[7] = s7;
}

void adcCallback(){
	key = getADCKeyAct(enumADCKey3);
	if(key == enumKeyPress){ // 切换显示模式
		show_state = (show_state + 1)%3;
	}
	key = getADCKeyAct(enumADCKeyCenter);
	if(key == enumKeyPress){ // 切换设置模式
		is_setting = (1 - is_setting);
	}
	
	if(is_setting == 1){ // 只有在设置模式，其他导航键才有效
		key = getADCKeyAct(enumADCKeyLeft);
		if(key == enumKeyPress){
			if(set_pos<2)set_pos++;
		}
		key = getADCKeyAct(enumADCKeyRight);
		if(key == enumKeyPress){
			if(set_pos>0)set_pos--;
		}
		key = getADCKeyAct(enumADCKeyUp);
		if(key == enumKeyPress){
			if(show_state == 0){// 速度
				if(speed[set_pos] < 255)speed[set_pos]++;
			}
			else if(show_state == 1){ // 加速度
				if(acc[set_pos] < 10)acc[set_pos]++;
			}
			else if(show_state == 2){ // 方向
				if(dir[set_pos] == 0)dir[set_pos] = 1;
			}
		}
		key = getADCKeyAct(enumADCKeyDown);
		if(key == enumKeyPress){
			if(show_state == 0){// 速度
				if(speed[set_pos] > 0)speed[set_pos]--;
			}
			else if(show_state == 1){ // 加速度
				if(acc[set_pos] > -10)acc[set_pos]--;
			}
			else if(show_state == 2){ // 方向
				if(dir[set_pos] == 1)dir[set_pos] = 0;
			}
		}
	}
	
	// 每次按键后，更新sm的状态
	for(i=0;i<3;i++){
		if(_acc[i] == 0){ // 只有加速度为0时设置
			setSm(i, speed[i], 10000, dir[i]);
		}
		else{ // 加速度不为0时由真实速度设置speed
			speed[i] = _speeds[i];
		}
		setAcc(i, acc[i]);
	}
}

void setBuf(char s0,char s1,char s2,char s3,char s4,char s5,char s6,char s7){
	buf[0] = s0;
	buf[1] = s1;
	buf[2] = s2;
	buf[3] = s3;
	buf[4] = s4;
	buf[5] = s5;
	buf[6] = s6;
	buf[7] = s7;
}

void keyCallback(){
	// setBuf(0xaa,0x55,0x04,acc_state,0,0,0,0);
	// uart1Send(buf, 8);
	key = getKeyAct(enumKey1);
	if(key == enumKeyPress){
		if(acc_state == 1)acc_state = 0;
		else acc_state = 1;
	}
	key = getKeyAct(enumKey2);
	if(key == enumKeyPress){
		if(acc_state == 2)acc_state = 0;
		else acc_state = 2;
	}
	
	if(acc_state == 1){
		setAcc(0,5);
		setAcc(1,5);
		setAcc(2,5);
	}
	else if(acc_state == 2){
		setAcc(0,-5);
		setAcc(1,-5);
		setAcc(2,-5);
	}
	else if(acc_state == 0){
		setAcc(0,0);
		setAcc(1,0);
		setAcc(2,0);
	}
}



xdata unsigned char recv[8];
void setRecv(char s0,char s1,char s2,char s3,char s4,char s5,char s6,char s7){
	recv[0] = s0;
	recv[1] = s1;
	recv[2] = s2;
	recv[3] = s3;
	recv[4] = s4;
	recv[5] = s5;
	recv[6] = s6;
	recv[7] = s7;
}

void uart1Callback(){
	setRecv(rcv[0],rcv[1],rcv[2],rcv[3],rcv[4],rcv[5],rcv[6],rcv[7]); // 这里先copy数据
	// recv[7]是无效字节0x00，那它用来判断是否成功接收到数据，返回0x01
	recv[7] = 0x01;
	uart1Send(recv, 8);
	if(recv[2]>=0 && recv[2]<=2){ // 设置sm的情况
		// 优先设置加速度
		if(recv[4] != 0xff){
			setAcc(recv[2], recv[4]);
		}
		else if(recv[6] != 0xff){ // 加速度为0 平缓加速不为0，设置
			setSpeed(recv[2], recv[6]);
		}
		else{ // 其他情况设置
			setSm(recv[2], recv[3], 60000, recv[5]);
		}
	}
	else if(recv[2] == 0x03){ // 其他指令
		if(recv[3] == 0x00){ // 设置步数为60000
			setSm(0, _speeds[0], (recv[4]<<8)+recv[5], _dirs[0]);
			setSm(1, _speeds[1], (recv[4]<<8)+recv[5], _dirs[1]);
			setSm(2, _speeds[2], (recv[4]<<8)+recv[5], _dirs[2]);
		}
	}
}
	

xdata char tmp[3];
xdata char uart_turn = 0;
void int100Callback(){
	if(show_state == 0){
		ssb(_speeds[2]>>4,_speeds[2]&0x0f,46,_speeds[1]>>4,_speeds[1]&0x0f,46,_speeds[0]>>4,_speeds[0]&0x0f);
	}
	else if(show_state == 1){
		tmp[0] = _acc[0]+10;
		tmp[1] = _acc[1]+10;
		tmp[2] = _acc[2]+10;
		ssb(tmp[2]>>4,tmp[2]&0x0f,46,tmp[1]>>4,tmp[1]&0x0f,46,tmp[0]>>4,tmp[0]&0x0f);
	}
	else if(show_state == 2){
		ssb(0,_dirs[2],46,0,_dirs[1],46,0,_dirs[0]);
	}
	
	
	if(is_setting == 1){ // 加小数点
		if(seg_buf[7 - set_pos*3] < 10)seg_buf[7 - set_pos*3]+=16;
		else seg_buf[7 - set_pos*3]+=38;
	}
	
	setSeg(seg_buf[0],seg_buf[1],seg_buf[2],seg_buf[3],seg_buf[4],seg_buf[5],seg_buf[6],seg_buf[7]);
	
	if(uart_turn%3 == 0){ // 每300ms发送一次，三个sm的信息会在900ms后全部更新
		setBuf(0xaa,0x55,uart_turn/3,_speeds[uart_turn/3],_acc[uart_turn/3],_dirs[uart_turn/3],_steps[uart_turn/3]>>8,_steps[uart_turn/3]&0x00ff);
		uart1Send(buf, 8);
	}

	
	uart_turn = (uart_turn+1)%9;
	
}



void int1000Callback(){
	unsigned char teml,temh,litl,lith;
	adc = getAdc();
	temh = adc.adcTem>>8;
	teml = adc.adcTem&0x00ff;
	lith = adc.adcLum>>8;
	litl = adc.adcLum&0x00ff;
	
	setBuf(0xaa,0x55,0x03,temh,teml,lith,litl,0x00);
	uart1Send(buf, 8);
	
	if(adc.adcLum >= 100 | adc.adcLum <= 20){
		for(i=0;i<3;i++){
			if(_speeds[i]>30){
				setSpeed(i, 30);
			}
		}
	}
}

void main(){
	sysInit();
	smInit();
	disInit();
	adcInit();
	uart1Init(9600);
	setUart1Buf(rcv, 8, head, 2);
	
	setSm(0, speed[0], 60000, dir[0]);
	setSm(1, speed[1], 60000, dir[1]);
	setSm(2, speed[2], 60000, dir[2]);
	
	setLed(0x00);
	setSeg(46,46,46,46,46,46,46,46);
	
	setCallback(enumEventKey, keyCallback);
	setCallback(enumEventAdcKey, adcCallback);
	setCallback(enumEventInt100, int100Callback);
	setCallback(enumEventUart1, uart1Callback);
	setCallback(enumEventInt1000, int1000Callback);
	
	while(1){
		sysRun();
	}
}