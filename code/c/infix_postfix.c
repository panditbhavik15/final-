
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
