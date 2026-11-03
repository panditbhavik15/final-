
#include <stdio.h>
#include <stdlib.h>
struct node{ char d; struct node *l,*r; };
struct node* mk(char c){ struct node *n=malloc(sizeof *n); n->d=c; n->l=n->r=NULL; return n; }
void pre(struct node*t){ if(!t)return; printf("%c ",t->d); pre(t->l); pre(t->r); }
void in(struct node*t){ if(!t)return; in(t->l); printf("%c ",t->d); in(t->r); }
void post(struct node*t){ if(!t)return; post(t->l); post(t->r); printf("%c ",t->d); }
int height(struct node*t){ if(!t)return -1; int a=height(t->l),b=height(t->r); return 1+(a>b?a:b); }
int nodes(struct node*t){ if(!t)return 0; return 1+nodes(t->l)+nodes(t->r); }
int leaves(struct node*t){ if(!t)return 0; if(!t->l&&!t->r)return 1; return leaves(t->l)+leaves(t->r); }
int main(void){
    /* the tree on page 11-13 of the Unit 3 notes */
    struct node *A=mk('A'),*B=mk('B'),*C=mk('C'),*D=mk('D'),*E=mk('E'),*F=mk('F'),
                *G=mk('G'),*H=mk('H'),*J=mk('J'),*K=mk('K'),*L=mk('L'),*M=mk('M'),*O=mk('O');
    A->l=B; A->r=C; B->l=D; B->r=E; E->l=F; C->l=G; C->r=H;
    H->l=J; H->r=K; J->l=L; J->r=M; K->l=O;
    printf("   pre  : "); pre(A); printf("\n");
    printf("   in   : "); in(A);  printf("\n");
    printf("   post : "); post(A); printf("\n");
    printf("   height=%d  nodes=%d  leaves=%d\n", height(A), nodes(A), leaves(A));
    return 0;
}
