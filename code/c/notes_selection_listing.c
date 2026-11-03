
/* This is the program the notes print under the heading "Selection Sort".
   It compares and swaps inside the inner loop, which makes it EXCHANGE sort.
   Output is shown as-is so the difference is visible. */
#include <stdio.h>
int main(void){
    int a[]={24,6,2,97,0}, n=5, i, j, t;
    for(i=0;i<n-1;i++)
        for(j=i+1;j<n;j++)
            if(a[j]<a[i]){ t=a[i]; a[i]=a[j]; a[j]=t; }
    printf("   (listing labelled 'Selection Sort' in the notes) -> ");
    for(i=0;i<n;i++) printf("%4d", a[i]);
    printf("\n");
    return 0;
}
