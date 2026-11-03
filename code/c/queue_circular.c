
#include <stdio.h>
#define MAX 5
int q[MAX], front=-1, rear=-1;
void insert(int v){
    if((rear+1)%MAX==front){ printf("insert %d -> Queue Overflow\n", v); return; }
    if(front==-1) front=0;
    rear=(rear+1)%MAX; q[rear]=v;
    printf("insert %d -> ok, front=%d rear=%d\n", v, front, rear);
}
int del(void){
    if(front==-1){ printf("delete -> Queue Underflow\n"); return -1; }
    int v=q[front];
    if(front==rear) front=rear=-1; else front=(front+1)%MAX;
    printf("delete -> %d, front=%d rear=%d\n", v, front, rear);
    return v;
}
int main(void){
    int i;
    for(i=1;i<=6;i++) insert(i*10);
    for(i=1;i<=3;i++) del();
    for(i=7;i<=9;i++) insert(i*10);
    while(front!=-1) del();
    del();
    return 0;
}
