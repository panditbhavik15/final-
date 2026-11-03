
#include <stdio.h>
#include <stdlib.h>
struct node{ int d; struct node *l,*r; };
struct node* ins(struct node*t,int v){
    if(!t){ struct node*n=malloc(sizeof *n); n->d=v; n->l=n->r=NULL; return n; }
    if(v<t->d) t->l=ins(t->l,v); else if(v>t->d) t->r=ins(t->r,v);
    return t;
}
void ino(struct node*t,int *c){ if(!t)return; ino(t->l,c); printf("%d ",t->d); (*c)++; ino(t->r,c); }
int search(struct node*t,int v,int *cmp){
    (*cmp)++;
    if(!t) return 0;
    if(t->d==v) return 1;
    return v<t->d ? search(t->l,v,cmp) : search(t->r,v,cmp);
}
int main(void){
    struct node *t=NULL; int i, v[]={50,30,70,20,40,60,80}, c, cmp, q[]={20,80,65,50};
    for(i=0;i<7;i++) t=ins(t,v[i]);
    c=0; printf("   in-order (sorted): "); ino(t,&c); printf("\n");
    for(i=0;i<4;i++){ cmp=0; int f=search(t,q[i],&cmp);
        printf("   search %2d -> %-9s comparisons=%d\n", q[i], f?"FOUND":"not present", cmp); }
    return 0;
}
