
#include <stdio.h>
int main(void){
    int a[]={15,22,35,48,60,72,85}, n=7, target, lo, hi, mid, cmp, found;
    int t[3]={72, 15, 99};
    for(int s=0;s<3;s++){
        target=t[s]; lo=0; hi=n-1; cmp=0; found=-1;
        while(lo<=hi){
            mid=(lo+hi)/2; cmp++;
            printf("   target %2d: lo=%d hi=%d mid=%d a[mid]=%2d  ", target, lo, hi, mid, a[mid]);
            if(a[mid]==target){ found=mid; printf("MATCH\n"); break; }
            if(a[mid]<target){ lo=mid+1; printf("go right\n"); }
            else { hi=mid-1; printf("go left\n"); }
        }
        printf("   target %2d -> %s in %d comparison(s)\n\n", target,
               found<0?"NOT FOUND":"found", cmp);
    }
    return 0;
}
