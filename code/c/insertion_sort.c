
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
