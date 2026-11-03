
#include <stdio.h>
int main(void){
    int a[3][4]={{1,2,3,4},{5,6,7,8},{9,10,11,12}};
    int base=1000, w=2, i, j;
    printf("   row-major walk of a[3][4]:\n");
    for(i=0;i<3;i++){ printf("     "); for(j=0;j<4;j++) printf("%4d", a[i][j]); printf("\n"); }
    printf("   LOC(i,j) = %d + ((i-1)*4 + (j-1)) * %d   (indices 1..3, 1..4)\n", base, w);
    for(i=1;i<=3;i++) for(j=1;j<=4;j++)
        printf("     LOC(%d,%d)=%d  value %d\n", i, j,
               base + ((i-1)*4 + (j-1))*w, a[i-1][j-1]);
    return 0;
}
