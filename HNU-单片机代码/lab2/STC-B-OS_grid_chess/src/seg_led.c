#include "seg_led.h"

XDATA u8 seg_display_content[8] = {0,0,0,0,0,0,0,0};
XDATA u8 led_display_content = 0;
XDATA u8 seg_led_current = 0;


// CODE u8 seg_decoder[128] ={
//     0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f, 0x77,0x7c,0x39,0x5e,0x79,0x71,      //hex 0~F
//     0, 0, 0, 0, 0, 0, 0, 0,     0, 0, 0, 0, 0, 0, 0, 0,

//     0x00, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x00, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, //space and others
//     0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f,                                     //numbers
//     0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,                                                       //others
//     0x77,0x7c,0x39,0x5e,0x79,0x71,0x3d,0x76,0x0f,0x0e,0x75,0x38,0x37,0x54,0x5c,0x73,0x67,0x31,0x6d/*s:0x49, 5:0x6d*/,0x78,0x3e,0x1c,0x7e,0x64,0x6e,0x59, //A-Z
//     0x80, 0x80, 0x80, 0x80, 0x80, 0x80,                                                             //others
//     0x77,0x7c,0x39,0x5e,0x79,0x71,0x3d,0x76,0x0f,0x0e,0x75,0x38,0x37,0x54,0x5c,0x73,0x67,0x31,0x6d/*s:0x49, 5:0x6d*/,0x78,0x3e,0x1c,0x7e,0x64,0x6e,0x59, //a-z
//     0x80, 0x80, 0x80, 0x80, 0x80                                                                    //others
// };
CODE u8 seg_decoder[] = { 
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

void setSegAdd(u8 weixuan, u8 duanxuan) large reentrant{
    seg_display_content[weixuan] |= (1<<duanxuan);
}

void setSegDir(u8 s0, u8 s1, u8 s2, u8 s3, u8 s4, u8 s5, u8 s6, u8 s7) large reentrant{
	seg_display_content[0] = s0;
	seg_display_content[1] = s1;
	seg_display_content[2] = s2;
	seg_display_content[3] = s3;
	seg_display_content[4] = s4;
	seg_display_content[5] = s5;
	seg_display_content[6] = s6;
	seg_display_content[7] = s7;
}

void setSeg(u8 s0, u8 s1, u8 s2, u8 s3, u8 s4, u8 s5, u8 s6, u8 s7) large reentrant
{
	seg_display_content[0] = seg_decoder[s0];
	seg_display_content[1] = seg_decoder[s1];
	seg_display_content[2] = seg_decoder[s2];
	seg_display_content[3] = seg_decoder[s3];
	seg_display_content[4] = seg_decoder[s4];
	seg_display_content[5] = seg_decoder[s5];
	seg_display_content[6] = seg_decoder[s6];
	seg_display_content[7] = seg_decoder[s7];
}

void seg_set_str(char* str) large reentrant
{
	seg_display_content[0] = seg_decoder[str[0]];
	seg_display_content[1] = seg_decoder[str[1]];
	seg_display_content[2] = seg_decoder[str[2]];
	seg_display_content[3] = seg_decoder[str[3]];
	seg_display_content[4] = seg_decoder[str[4]];
	seg_display_content[5] = seg_decoder[str[5]];
	seg_display_content[6] = seg_decoder[str[6]];
	seg_display_content[7] = seg_decoder[str[7]];
}

void seg_set_number(u32 n) large reentrant
{
    seg_display_content[7] = seg_decoder[n%10]; n/=10;
    seg_display_content[6] = seg_decoder[n%10]; n/=10;
    seg_display_content[5] = seg_decoder[n%10]; n/=10;
    seg_display_content[4] = seg_decoder[n%10]; n/=10;
    seg_display_content[3] = seg_decoder[n%10]; n/=10;
    seg_display_content[2] = seg_decoder[n%10]; n/=10;
    seg_display_content[1] = seg_decoder[n%10]; n/=10;
    seg_display_content[0] = seg_decoder[n%10]; n/=10;
}

//this function should be called in system timer ISR
//no reentrancy is supported
void seg_led_scan_next()
{
    switch(seg_led_current)
    {
        case 0: DISP_SEG(0)     seg_led_current++; break;
        case 1: DISP_SEG(1)     seg_led_current++; break;
        case 2: DISP_SEG(2)     seg_led_current++; break;
        case 3: DISP_SEG(3)     seg_led_current++; break;
        case 4: DISP_SEG(4)     seg_led_current++; break;
        case 5: DISP_SEG(5)     seg_led_current++; break;
        case 6: DISP_SEG(6)     seg_led_current++; break;
        case 7: DISP_SEG(7)     seg_led_current++; break;
        case 8: DISP_LED()      seg_led_current=0; break;
		default: seg_led_current = 0;
    }
}