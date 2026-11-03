
#include <stdio.h>
#include <stdlib.h>
struct node{ struct node *prev; int data; struct node *next; };
struct node *head=NULL;
void append(int v){
    struct node *n=malloc(sizeof *n); n->data=v; n->next=NULL; n->prev=head;
    if(head) head->next=n; head=n;
}
void forward(void){ struct node *p=head; while(p){ printf("%d ",p->data); p=p->prev; } printf("\n"); }
int main(void){
    int i, in[]={10,20,30,40,50};
    for(i=0;i<5;i++) append(in[i]);
    printf("appended 10,20,30,40,50; walking from the tail through prev:\n   ");
    forward();
    return 0;
}
