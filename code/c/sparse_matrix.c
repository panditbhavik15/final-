
#include <stdio.h>
int main(void){
    int a[4][4]={{0,0,5,0},{0,8,0,0},{0,0,0,3},{9,0,0,0}};
    int t[3][10], i, j, n=0;
    printf("   4x4 matrix (16 cells):\n");
    for(i=0;i<4;i++){ printf("     "); for(j=0;j<4;j++) printf("%3d", a[i][j]); printf("\n"); }
    for(i=0;i<4;i++) for(j=0;j<4;j++) if(a[i][j]){ t[0][n]=i; t[1][n]=j; t[2][n]=a[i][j]; n++; }
    t[0][n]=4; t[1][n]=4; t[2][n]=n;
    printf("   triplet form (row, col, value):\n      row : ");
    for(i=0;i<=n;i++) printf("%3d", t[0][i]);
    printf("\n      col : ");
    for(i=0;i<=n;i++) printf("%3d", t[1][i]);
    printf("\n      val : ");
    for(i=0;i<=n;i++) printf("%3d", t[2][i]);
    printf("\n");
    printf("   stored cells = 3*(%d+1) = %d instead of 16\n", n, 3*(n+1));
    return 0;
}
