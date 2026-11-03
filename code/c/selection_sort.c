
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
