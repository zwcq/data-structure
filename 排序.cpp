#include <stdio.h>
#include <stdlib.h>

void print_list(int a[])
{
    for (int i = 1; i < 11; i++)
        printf("%d-", a[i]);
    printf("\n");
}

void insert_sort(int a[])
{
    int i, j;
    for (i = 2; i < 11; i++)
    {
        if(a[i] < a[i-1])
        {
            a[0] = a[i];
            for (j = i - 1; a[j] > a[0]; j--)
                a[j + 1] = a[j];
            a[j + 1] = a[0];
        }
    }
}

void banary_insert_sort(int a[])
{
    int low, high, mid, i;
    for (i = 2; i < 11; i++)
    {
        if(a[i] < a[i - 1])
        {
            a[0] = a[i];
            low = 1;
            high = i - 1;
            while (low <= high)
            {
                mid = (low + high) / 2;
                if(a[0] >= a[mid])
                    low = mid + 1;
                else
                    high = mid - 1;
            }
            for (int j = i - 1; j >= low; j--)
                a[j + 1] = a[j];
            a[low] = a[0];
        }
    }
}

int shell_dk[3] = {5, 2, 1};
void shell_sort(int a[])
{
    int i, j, k, dk;
    for (j = 1; j < 3; j++)
    {
        dk = shell_dk[j];
        for (i = dk + 1; i < 11; i++)
        {
            if(a[i] < a[i - dk])
            {
                a[0] = a[i];
                for (k = i - dk; k > 0 && a[k] > a[0]; k-=dk)
                    a[k + dk] = a[k];
                a[k + dk] = a[0];
            }
        }
    }  
}

void bubble_sort(int a[])
{
    int i, j, flag = 1, swap;
    for (j = 1; j < 11; j++)
    {
        flag = 0;
        for (i = 1; i < 11 - j; i++)
        {
            if(a[i] > a[i+1])
            {
                flag = 1;
                swap = a[i];
                a[i] = a[i + 1];
                a[i + 1] = swap;
            }
            // printf("第%d次\n", i);
            // print_list(a);
        }
        if(flag == 0)
            return ;
    }
}

int partition(int a[], int low, int high)
{
    int pivot = a[low];
    while(low < high)
    {
        while(low < high && a[high] >= pivot)
            high--;
        a[low] = a[high];
        while(low < high && a[low] <= pivot)
            low++;
        a[high] = a[low];
    }
    a[low] = pivot;//别忘记放到所属位置
    // printf("轴是%d\n", pivot);
    // print_list(a);
    return low;
}

void quick_sort(int a[], int low, int high)
{
    if(low < high)
    {
        int pivot_pos = partition(a, low, high);
        quick_sort(a, low, pivot_pos - 1);
        quick_sort(a, pivot_pos + 1, high);
    }
}

void simple_select_sort(int a[])
{
    int i, j, min, temp;
    for (j = 1; j < 11; j++)
    {
        min = j;
        for (i = j + 1; i < 11; i++)
            if (a[i] < a[min])
                min = i;
        if(min != j)//如果相等，则不执行交换，省下不做判断时交换的时间
        {
            temp = a[j];
            a[j] = a[min];
            a[min] = temp;
        }  
    }
}

void head_adjust(int a[], int i, int len)
{
    int j;
    a[0] = a[i];
    for (j = 2 * i; j <= len; j = 2 * j)//遍历以i为根节点的树所有子节点，如果只比较他的孩子节点，则可能会遗漏他的孙节点比他大的可能。比如a[6]={0, 6, 9, 5, 8, 7}
    {
        if(j < len && a[j] < a[j + 1])
            j++;
        if(a[0] > a[j])
            break;
        else
        {
            a[i] = a[j];
            i = j;
        }
    }        
    a[i] = a[0];
}

void build_max_heap(int a[] ,int len)
{
    int i;
    for (i = len / 2; i > 0; i--)
        head_adjust(a, i, len);
}

void heap_sort(int a[])
{
    int i, len = 10, temp = -1;
    for (i = len; i > 0; i--)
    {
        temp = a[1];
        a[1] = a[i];
        a[i] = temp;
        head_adjust(a, 1, i - 1);    
    }
}

int merge_list[11];
void merge(int a[], int low, int mid, int high)
{
    int i, j, k;
    for (int i = low; i <= high; i++)
        merge_list[i] = a[i];
    for (i = low, j = mid + 1, k = low; i <= mid && j <= high; k++)
    {
        if(merge_list[i] <= merge_list[j])
            a[k] = merge_list[i++];
        else
            a[k] = merge_list[j++];
    }
    while(i <= mid)
        a[k++] = merge_list[i++];
    while(j <= high)
        a[k++] = merge_list[j++];
}

void merge_sort(int a[], int low, int high)
{
    if(low < high)
    {
        int mid = (low + high) / 2;
        merge_sort(a, low, mid);
        merge_sort(a, mid + 1, high);
        merge(a, low, mid, high);
    }  
}

int main()
{
    int a[11];
    for (int i = 0; i < 11; i++)
        a[i] = rand() % 10;
    print_list(a);
    // insert_sort(a);
    // banary_insert_sort(a);
    // shell_sort(a);
    // bubble_sort(a);
    // quick_sort(a, 1, 10);
    // simple_select_sort(a);
    // build_max_heap(a, 10);
    // print_list(a);
    // heap_sort(a);
    merge_sort(a, 1, 10);
    print_list(a);
}