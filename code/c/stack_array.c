
#include <stdio.h>
#define MAX 5
int st[MAX], top = -1;
void push(int v){
    if(top==MAX-1){ printf("push %d -> Overflow\n", v); return; }
    st[++top]=v; printf("push %d -> ok, top=%d\n", v, st[top]);
}
void pop(void){
    if(top==-1){ printf("pop   -> Underflow\n"); return; }
    printf("pop   -> %d\n", st[top--]);
}
void peep(void){
    if(top==-1){ printf("peep  -> the stack is empty\n"); return; }
    printf("peep  -> %d\n", st[top]);
}
int main(void){
    int i;
    for(i=1;i<=6;i++) push(i*10);
    peep();
    for(i=1;i<=7;i++) pop();
    peep();
    return 0;
}
