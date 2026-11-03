
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
