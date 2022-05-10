#include <stdio.h>
#include <stdlib.h>
#define MaxSize 10
typedef struct{
    int data[MaxSize];
    int length;
} SqList;

void Initlist(SqList &L)
{
    for (int i = 0; i < MaxSize; i++)
    {
        L.data[i] = 0;
    }
    L.length = 0;
}

bool ListInsert(SqList &L, int i, int e)
{
    if(i>L.length || i < 1 || L.length == MaxSize)
        return false;
    for (int j = L.length; j >= i; j--)
        L.data[j] = L.data[j - 1];
    L.data[i - 1] = e;
    L.length++;
    return true;
}

bool ListDel(SqList &L, int i, int &e)
{
    if(i>L.length || i < 1)
        return false;
    e = L.data[i - 1];
    for (int j = i; j < L.length; j++)
        L.data[j - 1] = L.data[j];
    L.length--;
    return true;
}

int Listindex(SqList &L, int i)
{
    return L.data[i - 1];
}

int Listval(SqList &L, int i)
{
    for (int j = 0; j < L.length; j++)
        if(L.data[j] == i)
            return j + 1;
    return 0;
}

void printList(SqList &L)
{
    for (int i = 0; i < L.length; i++)
        printf("%d ", L.data[i]);
    printf("\n");
}

bool delete_val(SqList &L, int s, int t)
{
    if(L.length == 0 || s > t)
        return false;
    int quick, slow;
    quick = slow = 0;
    while (quick < L.length)
    {
        if(L.data[quick] > t || L.data[quick] < s)
        {
            L.data[slow] = L.data[quick];
            slow++;
        }
        quick++;
    }
    L.length = slow;
    return true;
}

void delete_chongfu(SqList &L)
{
    int tail = L.length - 1;
    int slow, quick;
    slow = L.length - 1;
    while(slow > 0)
    {
        for (quick = slow - 1; quick >= 0; quick--)
        {
            
            if(L.data[slow] == L.data[quick])
            {
                if(slow != tail)
                    L.data[slow] = L.data[tail];
                tail--;
                L.length--;
                quick = -1;//找到一个立马退出
            }

        }
        slow--;
    }
}

void delete_chongfu1(SqList &L)//o（n^2）,快指针定插入数字，慢指针定插入位置，这样是o（n），顺序表才能这么做，无序表得用散列来
{
    int slow, quick;
    slow = L.length - 1;
    while(slow > 0)
    {
        quick = slow - 1;
        if(L.data[quick] == L.data[slow])
        {
            while(L.data[quick - 1] == L.data[slow])
                quick--;
            int j = quick + 1;
            for (int i = slow + 1; i < L.length; i++)
            {
                L.data[j] = L.data[i];
                j++;
            }
            L.length -= (slow - quick);
            slow = quick - 1;
        }
        else
            slow--;
        
    }
}

int main()
{
    SqList L;
    Initlist(L);
    int nums[6] = {1,1,1,1,1,1};
    for (int i = 0; i < 6; i++)
    {
        L.data[i] = nums[i];
    }
    L.length = 6;
    // printList(L);
    // if(ListInsert(L, 3, 3))
    //     printf("插入成功，插入位序是%d，插入的是%d\n", 3, 3);
    // else
    //     printf("插入失败\n");
    // printList(L);
    // int e = -1;
    // if(ListDel(L, 4, e))
    //     printf("删除成功，删除位序是%d，删除的是%d\n", 4, e);l
    // else
    //     printf("删除失败\n");
    // printList(L);
    // printf("%d\n", Listindex(L, 4));
    // printf("%d\n", Listval(L, 3));
    // if(delete_val(L, 1, 5))
    //     printList(L);
    // else
    //     printf("删除失败\n");
    // delete_chongfu(L);
    delete_chongfu1(L);
    printList(L);
    printf("表长为%d\n", L.length);
    return 0;
}
