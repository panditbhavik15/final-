
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
