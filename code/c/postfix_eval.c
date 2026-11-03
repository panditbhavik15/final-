
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
