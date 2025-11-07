#ifndef __MUTEX_H__
#define __MUTEX_H__

#include "global.h"
#include "syscall.h"
#include "intrins.h"

#define DISABLE_INTERRUPTS()   {EA = 0; ET0 = 0;}
#define ENABLE_INTERRUPTS()    {EA = 1; ET0 = 1;}

// #define DISABLE_INTERRUPTS()   {flag_nosched = 1;}
// #define ENABLE_INTERRUPTS()    {flag_nosched = 0;}

#ifndef NULL

#define NULL ((void*)0)

#endif

// 比较并交换
typedef struct lock_t{
    u8 ticket;
    u8 turn;
} lock_t;

// 测试并设置
// typedef struct lock_t{
//     u8 flag;
// } lock_t;

void lock_init(lock_t* lock);
void lock(lock_t* lock);
void unlock(lock_t* lock);

#endif