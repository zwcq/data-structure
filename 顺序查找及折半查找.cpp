#include <stdio.h>

int search_seq(int a[], int key, int len)//子函数里用sizeof算数组长度会算不对，因为参数中的数组退化成了指针，sizeof算得是指针的长度
{
    int i = len - 1;
    for (; a[i] != key && i >= 0; i--)
        ;
    if(a[i] == key)
        return i;
    else
        return -1;
}

int banary_sreach(int a[], int key, int len)
{
    int low = 0;
    int high = len - 1;
    while(low <= high)
    {
        int mid = (low + high) / 2;
        if(a[mid] == key)
            return mid;
        else if(a[mid] > key)
            high = mid - 1;
        else
            low = mid + 1;
    }
    return -1;
}

int main()
{
    int a[6] = {123, 456, 789, 549, 555, 781};
    int up[6] = {7, 8, 9, 10, 11, 12};
    int len = sizeof(a) / sizeof(int);
    int len1 = sizeof(up) / sizeof(int);
    printf("%d\n", search_seq(a, 1203, len));
    printf("%d\n", banary_sreach(up, 12, len1));
    return 0;
}

