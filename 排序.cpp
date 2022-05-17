#include <stdio.h>
#include <stdlib.h>

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

void print_list(int a[])
{
    for (int i = 1; i < 11; i++)
        printf("%d-", a[i]);
    printf("\n");
}

int main()
{
    int a[11];
    for (int i = 0; i < 11; i++)
        a[i] = rand() % 10;
    print_list(a);
    // insert_sort(a);
    // banary_insert_sort(a);
    shell_sort(a);
    print_list(a);
}