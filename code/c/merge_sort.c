
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
