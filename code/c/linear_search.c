
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
