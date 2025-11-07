#include "mutex.h"

// 比较并交换
void lock_init(lock_t* lock){
    lock->ticket = 0;
    lock->turn = 0;
}

void lock(lock_t* lock){
    u8 myturn;

    DISABLE_INTERRUPTS();
    myturn = lock->ticket; // 设置当前进程的回合
    
    lock->ticket = lock->ticket+1;
    ENABLE_INTERRUPTS();

    while(lock->turn != myturn){ // 如果没有到当前回合，放弃时间片
        proc_yield();
    }

    proc_sleep(1);
}

void unlock(lock_t* lock){
    DISABLE_INTERRUPTS();
    lock->turn = lock->turn+1;
    ENABLE_INTERRUPTS();

    proc_sleep(1);
}

// 测试并设置
// void lock_init(lock_t* mut){
//     mut->flag = 0;
// }

// void lock(lock_t* mut){
//     u8 tmp = 1;
//     while(tmp == 1){
//         DISABLE_INTERRUPTS();
//         if(mut->flag == 0){
//             mut->flag = 1;
//             tmp = 0;
//         } 
//         ENABLE_INTERRUPTS();
//     }
//     proc_sleep(1);
// }

// void unlock(lock_t* mut){
//     DISABLE_INTERRUPTS();
//     mut->flag = 0;
//     ENABLE_INTERRUPTS();

//     proc_sleep(1);
// }