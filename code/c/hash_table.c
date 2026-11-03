
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
