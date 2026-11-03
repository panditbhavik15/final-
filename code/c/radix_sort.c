
#include <stdio.h>
#define N 14
int main(void){
    int a[N]={42,23,74,17,65,57,94,36,99,87,70,81,64,22}, out[N], b[10], i, d, div=1;
    for(d=0; d<2; d++){
        for(i=0;i<10;i++) b[i]=0;
        for(i=0;i<N;i++) b[(a[i]/div)%10]++;
        for(i=1;i<10;i++) b[i]+=b[i-1];
        for(i=N-1;i>=0;i--) out[--b[(a[i]/div)%10]] = a[i];
        for(i=0;i<N;i++) a[i]=out[i];
        printf("   pass %d (place %d): ", d+1, div);
        for(i=0;i<N;i++) printf("%3d", a[i]);
        printf("\n");
        div*=10;
    }
    printf("   sorted: ");
    for(i=0;i<N;i++) printf("%3d", a[i]);
    printf("\n");
    return 0;
}
