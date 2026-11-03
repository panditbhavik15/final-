
#include <stdio.h>
#include <stdlib.h>
struct node{ int data; struct node *next; };
struct node *head=NULL;
void insert_front(int v){ struct node *n=malloc(sizeof *n); n->data=v; n->next=head; head=n; }
void insert_end(int v){
    struct node *n=malloc(sizeof *n); n->data=v; n->next=NULL;
    if(!head){head=n;return;} struct node *p=head; while(p->next)p=p->next; p->next=n;
}
void show(const char *tag){
    struct node *p=head; int cnt=0;
    printf("%s: ", tag);
    for(p=head;p;p=p->next){ printf("%d->",p->data); cnt++; }
    printf("NULL   (length %d)\n", cnt);
}
int search(int v){ int i=1; for(struct node*p=head;p;p=p->next,i++) if(p->data==v) return i; return -1; }
void del_val(int v){
    struct node *p=head,*q=NULL;
    while(p && p->data!=v){ q=p; p=p->next; }
    if(!p){ printf("delete %d -> not found\n", v); return; }
    if(q) q->next=p->next; else head=p->next;
    free(p);
    printf("delete %d -> done\n", v);
}
int main(void){
    int i, in[]={20,30,40};
    for(i=0;i<3;i++) insert_end(in[i]);
    show("after 20,30,40 at the end");
    insert_front(10); show("after 10 at the front");
    printf("search 30 -> position %d\n", search(30));
    printf("search 99 -> position %d\n", search(99));
    del_val(30); show("after deleting 30");
    del_val(10); show("after deleting the head 10");
    del_val(30);
    return 0;
}
