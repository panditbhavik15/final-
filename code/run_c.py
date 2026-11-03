"""Emit and compile the C programs used in the DS answer key.

Each listing in Data_Structures_2BTCO301_Question_Bank_Answer_Key.md is written here as
real C99 and compiled with clang -Wall -Wextra so that every listing is known to build.
Running the binaries is not possible on this machine (Device Guard blocks every freshly
built .exe), so the printed Output blocks come from the equivalent executed model in
ds/verify_ds.py, which implements the same algorithms step for step.
"""
import os
import pathlib
import shutil
import subprocess

# Point $CLANG at a clang, or put clang on PATH. Any clang 18+ or LLVM-MinGW build works.
CLANG = os.environ.get("CLANG") or shutil.which("clang") or ""
if not CLANG:
    raise SystemExit("clang not found: set $CLANG to the clang executable or put it on PATH")
HERE = pathlib.Path(__file__).with_name("c")
HERE.mkdir(exist_ok=True)

P = {}

P["stack_array.c"] = r"""
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
"""

P["queue_circular.c"] = r"""
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
"""

P["sll.c"] = r"""
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
"""

P["dll.c"] = r"""
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
"""

P["infix_postfix.c"] = r"""
#include <stdio.h>
#include <string.h>
#define MAX 50
char st[MAX]; int top=-1;
int prec(char c){ if(c=='^')return 3; if(c=='*'||c=='/')return 2; if(c=='+'||c=='-')return 1; return 0; }
void toPostfix(char *s){
    char out[MAX]; int k=0;
    for(int i=0; s[i]; i++){
        char c=s[i];
        if((c>='A'&&c<='Z')||(c>='a'&&c<='z')||(c>='0'&&c<='9')) out[k++]=c;
        else if(c=='(') st[++top]=c;
        else if(c==')'){ while(top!=-1&&st[top]!='(') out[k++]=st[top--]; top--; }
        else { while(top!=-1&&prec(st[top])>=prec(c)&&c!='^') out[k++]=st[top--];
               while(top!=-1&&c=='^'&&prec(st[top])>=prec(c)) out[k++]=st[top--];
               st[++top]=c; }
    }
    while(top!=-1) out[k++]=st[top--];
    out[k]='\0';
    printf("   infix  %-18s -> postfix %s\n", s, out);
}
int main(void){
    char a[]="A*(B+C)-D/E", b[]="(A-B)*(C+D)", c[]="(A+B)/(C+D)-(D*E)", d[]="A+B*C";
    toPostfix(a); toPostfix(b); toPostfix(c); toPostfix(d);
    return 0;
}
"""

P["postfix_eval.c"] = r"""
#include <stdio.h>
int main(void){
    char *e="934*8+4/-";
    int st[50], top=-1;
    for(int i=0; e[i]; i++){
        char c=e[i];
        if(c>='0'&&c<='9'){ st[++top]=c-'0'; printf("   read %c, stack: ", c); for(int k=0;k<=top;k++)printf("%d ",st[k]); printf("\n"); }
        else { int b=st[top--], a=st[top--], r; char op=c;
               if(op=='+')r=a+b; else if(op=='-')r=a-b; else if(op=='*')r=a*b; else r=a/b;
               st[++top]=r;
               printf("   %d %c %d = %d, stack: ", a, op, b, r);
               for(int k=0;k<=top;k++)printf("%d ",st[k]); printf("\n"); }
    }
    printf("   value of 9 3 4 * 8 + 4 / - = %d\n", st[top]);
    return 0;
}
"""

P["bubble_sort.c"] = r"""
#include <stdio.h>
int main(void){
    int a[]={78,23,45,8,32,36}, n=6, i, j, t, swaps;
    for(i=0;i<n-1;i++){
        swaps=0;
        for(j=0;j<n-1-i;j++) if(a[j]>a[j+1]){ t=a[j];a[j]=a[j+1];a[j+1]=t; swaps++; }
        printf("   pass %d: ", i+1);
        for(j=0;j<n;j++) printf("%4d", a[j]);
        printf("   swaps=%d\n", swaps);
        if(swaps==0){ printf("   no swap in this pass -> sorted, stopping early\n"); break; }
    }
    printf("   final : ");
    for(j=0;j<n;j++) printf("%4d", a[j]);
    printf("\n");
    return 0;
}
"""

P["notes_selection_listing.c"] = r"""
/* This is the program the notes print under the heading "Selection Sort".
   It compares and swaps inside the inner loop, which makes it EXCHANGE sort.
   Output is shown as-is so the difference is visible. */
#include <stdio.h>
int main(void){
    int a[]={24,6,2,97,0}, n=5, i, j, t;
    for(i=0;i<n-1;i++)
        for(j=i+1;j<n;j++)
            if(a[j]<a[i]){ t=a[i]; a[i]=a[j]; a[j]=t; }
    printf("   (listing labelled 'Selection Sort' in the notes) -> ");
    for(i=0;i<n;i++) printf("%4d", a[i]);
    printf("\n");
    return 0;
}
"""

P["selection_sort.c"] = r"""
#include <stdio.h>
int main(void){
    int a[]={11,2,9,3,1,25,17,57,90,13}, n=10, i, j, min, t;
    for(i=0;i<n-1;i++){
        min=i;
        for(j=i+1;j<n;j++) if(a[j]<a[min]) min=j;
        t=a[i]; a[i]=a[min]; a[min]=t;
        printf("   pass %2d: min %d at index %d, swap with index %d -> ", i+1, a[i], min, i);
        for(j=0;j<n;j++) printf("%3d", a[j]);
        printf("\n");
    }
    return 0;
}
"""

P["insertion_sort.c"] = r"""
#include <stdio.h>
int main(void){
    int a[]={24,6,2,97,0}, n=5, i, j, key;
    for(i=1;i<n;i++){
        key=a[i]; j=i-1;
        while(j>=0 && a[j]>key){ a[j+1]=a[j]; j--; }
        a[j+1]=key;
        printf("   take %3d -> ", key);
        for(j=0;j<n;j++) printf("%4d", a[j]);
        printf("\n");
    }
    return 0;
}
"""

P["merge_two.c"] = r"""
#include <stdio.h>
int main(void){
    int a[]={2,9,11,13,57}, b[]={1,3,17,25,90}, c[10];
    int i=0,j=0,k=0;
    while(i<5 && j<5) c[k++] = a[i]<=b[j] ? a[i++] : b[j++];
    while(i<5) c[k++]=a[i++];
    while(j<5) c[k++]=b[j++];
    printf("   a = 2 9 11 13 57\n   b = 1 3 17 25 90\n   c = ");
    for(i=0;i<10;i++) printf("%3d", c[i]);
    printf("\n");
    return 0;
}
"""

P["merge_sort.c"] = r"""
#include <stdio.h>
void merge(int a[],int l,int m,int r){
    int n1=m-l+1,n2=r-m, L[100], R[100], i,j,k;
    for(i=0;i<n1;i++)L[i]=a[l+i];
    for(j=0;j<n2;j++)R[j]=a[m+1+j];
    i=0;j=0;k=l;
    while(i<n1&&j<n2) a[k++]= L[i]<=R[j] ? L[i++] : R[j++];
    while(i<n1)a[k++]=L[i++];
    while(j<n2)a[k++]=R[j++];
}
void ms(int a[],int l,int r){
    if(l<r){ int m=(l+r)/2; ms(a,l,m); ms(a,m+1,r); merge(a,l,m,r);
             printf("   merged [%d..%d] and [%d..%d] -> ", l, m, m+1, r);
             for(int i=l;i<=r;i++) printf("%d ", a[i]); printf("\n"); }
}
int main(void){
    int a[]={38,27,43,3,9,82,10}, n=7, i;
    ms(a,0,n-1);
    printf("   sorted: ");
    for(i=0;i<n;i++) printf("%d ", a[i]);
    printf("\n");
    return 0;
}
"""

P["quick_sort.c"] = r"""
#include <stdio.h>
int partition(int a[],int lo,int hi){
    int p=a[hi], i=lo-1, j, t;
    for(j=lo;j<hi;j++) if(a[j]<=p){ i++; t=a[i];a[i]=a[j];a[j]=t; }
    t=a[i+1];a[i+1]=a[hi];a[hi]=t;
    printf("   pivot %d -> split point j=%d : ", p, i+1);
    for(j=0;j<=hi;j++) printf("%d ", a[j]);
    for(;j<7;j++) printf("%d ", a[j]);
    printf("\n");
    return i+1;
}
void qs(int a[],int lo,int hi){
    if(lo<hi){ int j=partition(a,lo,hi); qs(a,lo,j-1); qs(a,j+1,hi); }
}
int main(void){
    int a[]={1,8,9,4,7,2,6}, n=7, i;
    qs(a,0,n-1);
    printf("   sorted: ");
    for(i=0;i<n;i++) printf("%d ", a[i]);
    printf("\n");
    return 0;
}
"""

P["radix_sort.c"] = r"""
#include <stdio.h>
#define N 14
int main(void){
    int a[N]={42,23,74,17,65,57,94,36,99,87,70,81,64,22}, out[N], b[10], i, d, div=1;
    for(d=0; d<2; d++){
        for(i=0;i<10;i++) b[i]=0;
        for(i=0;i<N;i++) b[(a[i]/div)%10]++;
        for(i=1;i<10;i++) b[i]+=b[i-1];
        for(i=N-1;i>=0;i--) out[--b[(a[i]/div)%10]] = a[i];
        for(i=0;i<N;i++) a[i]=out[i];
        printf("   pass %d (place %d): ", d+1, div);
        for(i=0;i<N;i++) printf("%3d", a[i]);
        printf("\n");
        div*=10;
    }
    printf("   sorted: ");
    for(i=0;i<N;i++) printf("%3d", a[i]);
    printf("\n");
    return 0;
}
"""

P["linear_search.c"] = r"""
#include <stdio.h>
int main(void){
    int a[]={35,22,48,10,60,72,15}, n=7, target=72, i, pos=-1, cmp=0;
    for(i=0;i<n;i++){ cmp++; if(a[i]==target){ pos=i; break; } }
    printf("   searching for %d: comparisons=%d, index=%d (position %d)\n", target, cmp, pos, pos+1);
    target=99; cmp=0; pos=-1;
    for(i=0;i<n;i++){ cmp++; if(a[i]==target){ pos=i; break; } }
    printf("   searching for %d: comparisons=%d, %s\n", target, cmp, pos<0?"not found":"found");
    return 0;
}
"""

P["binary_search.c"] = r"""
#include <stdio.h>
int main(void){
    int a[]={15,22,35,48,60,72,85}, n=7, target, lo, hi, mid, cmp, found;
    int t[3]={72, 15, 99};
    for(int s=0;s<3;s++){
        target=t[s]; lo=0; hi=n-1; cmp=0; found=-1;
        while(lo<=hi){
            mid=(lo+hi)/2; cmp++;
            printf("   target %2d: lo=%d hi=%d mid=%d a[mid]=%2d  ", target, lo, hi, mid, a[mid]);
            if(a[mid]==target){ found=mid; printf("MATCH\n"); break; }
            if(a[mid]<target){ lo=mid+1; printf("go right\n"); }
            else { hi=mid-1; printf("go left\n"); }
        }
        printf("   target %2d -> %s in %d comparison(s)\n\n", target,
               found<0?"NOT FOUND":"found", cmp);
    }
    return 0;
}
"""

P["tree_traversal.c"] = r"""
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
"""

P["bst.c"] = r"""
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
"""

P["hash_table.c"] = r"""
#include <stdio.h>
#define M 10
int main(void){
    int t[M], i, j, k, key, pos, v[]={50,700,76,85,96,73,101,399,541}, n=9;
    for(i=0;i<M;i++) t[i]=-1;
    printf("   h(k) = k mod 10, linear probing, table size %d\n", M);
    for(i=0;i<n;i++){
        key=v[i]; pos=key%M; k=0;
        while(t[pos]!=-1){ pos=(pos+1)%M; k++; }
        t[pos]=key;
        printf("   insert %3d : h=%d, %d collision(s) -> stored at %d\n", key, key%M, k, pos);
    }
    printf("   table: ");
    for(i=0;i<M;i++) printf("%4d", t[i]);
    printf("\n");
    for(i=0;i<M;i++) t[i]=-1;
    printf("\n   same keys with chaining (bucket = k mod 10):\n");
    for(i=0;i<M;i++){
        int first=1;
        printf("   bucket %d :", i);
        for(j=0;j<n;j++) if(v[j]%M==i){ printf(" %d", v[j]); first=0; }
        if(first) printf(" empty");
        else { int cnt=0; for(j=0;j<n;j++) if(v[j]%M==i) cnt++; printf("   (chain length %d)", cnt); }
        printf("\n");
    }
    return 0;
}
"""

P["array_2d.c"] = r"""
#include <stdio.h>
int main(void){
    int a[3][4]={{1,2,3,4},{5,6,7,8},{9,10,11,12}};
    int base=1000, w=2, i, j;
    printf("   row-major walk of a[3][4]:\n");
    for(i=0;i<3;i++){ printf("     "); for(j=0;j<4;j++) printf("%4d", a[i][j]); printf("\n"); }
    printf("   LOC(i,j) = %d + ((i-1)*4 + (j-1)) * %d   (indices 1..3, 1..4)\n", base, w);
    for(i=1;i<=3;i++) for(j=1;j<=4;j++)
        printf("     LOC(%d,%d)=%d  value %d\n", i, j,
               base + ((i-1)*4 + (j-1))*w, a[i-1][j-1]);
    return 0;
}
"""

P["sparse_matrix.c"] = r"""
#include <stdio.h>
int main(void){
    int a[4][4]={{0,0,5,0},{0,8,0,0},{0,0,0,3},{9,0,0,0}};
    int t[3][10], i, j, n=0;
    printf("   4x4 matrix (16 cells):\n");
    for(i=0;i<4;i++){ printf("     "); for(j=0;j<4;j++) printf("%3d", a[i][j]); printf("\n"); }
    for(i=0;i<4;i++) for(j=0;j<4;j++) if(a[i][j]){ t[0][n]=i; t[1][n]=j; t[2][n]=a[i][j]; n++; }
    t[0][n]=4; t[1][n]=4; t[2][n]=n;
    printf("   triplet form (row, col, value):\n      row : ");
    for(i=0;i<=n;i++) printf("%3d", t[0][i]);
    printf("\n      col : ");
    for(i=0;i<=n;i++) printf("%3d", t[1][i]);
    printf("\n      val : ");
    for(i=0;i<=n;i++) printf("%3d", t[2][i]);
    printf("\n");
    printf("   stored cells = 3*(%d+1) = %d instead of 16\n", n, 3*(n+1));
    return 0;
}
"""


def main():
    log = []
    ok = 0
    for name, src in P.items():
        src_path = HERE / name
        exe = HERE / (name[:-2] + ".exe")
        src_path.write_text(src, encoding="utf-8")
        r = subprocess.run([CLANG, "-O0", "-std=c99", "-Wall", "-Wextra",
                            "-o", str(exe), str(src_path)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            log.append("### %s  COMPILE FAILED\n%s" % (name, r.stderr))
            continue
        ok += 1
        note = r.stderr.strip()
        # This machine's Device Guard policy blocks running any freshly built .exe,
        # so the programs are only compiled here. The printed output in the answer
        # key comes from the equivalent executed model in ds/verify_ds.py.
        log.append("### %-22s compiled clean%s" % (name, "" if not note else "  [warnings] " + note))
        try:
            exe.unlink()
        except OSError:
            pass
    text = "\n".join(log) + "\ncompiled %d/%d\n" % (ok, len(P))
    pathlib.Path(__file__).with_name("c_compile_check.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
