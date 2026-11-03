
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
