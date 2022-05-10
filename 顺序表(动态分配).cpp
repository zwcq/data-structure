#include <stdio.h>
#include <stdlib.h>
#define InitSize 10
typedef struct{
    int *data;
    int MaxSize;
    int length;
}SeqList;

void InitList(SeqList &L)//&是c++的引用
{
    L.data = (int *)malloc(sizeof(int) * InitSize);
    L.length = 0;
    L.MaxSize = InitSize;
}

void IncreaseSize(SeqList &L, int len)
{
    int *p = L.data;
    L.data = (int *)malloc(sizeof(int) * (InitSize + len));
    for (int i = 0; i < L.length; i++)
    {
        L.data[i] = p[i];
    }
    L.MaxSize = InitSize + len;
    free(p);
}

bool ListInsert(SeqList &L, int i, int e)
{
    if(i>L.length || i<1 || L.length == L.MaxSize)
        return false;
    for (int j = L.length; j >= i; j--)
        L.data[j] = L.data[j - 1];
    L.data[i - 1] = e;
    L.length += 1;
    return true;
}

bool ListDel(SeqList &L, int i, int &e)
{
    if(i>L.length || i<1 )
        return false;
    e = L.data[i - 1];
    for (int j = i; j < L.length; j++)
        L.data[j-1] = L.data[j];
    L.length--;
    return true;
}

int Listindex(SeqList &L, int i)
{
    return L.data[i - 1];
}

int Listval(SeqList &L, int e)
{
    for (int i = 0; i < L.length; i++)
        if(L.data[i] == e)
            return i + 1;
    return 0;
}

void printList(SeqList &L)
{
    for (int i = 0; i < L.length;i++)
        printf("%d ",L.data[i]);
    printf("\n");
    printf("长度为%d\n", L.length);
}

int main()
{
    SeqList L;
    InitList(L);
    int a[4] = {1, 2, 3, 4};
    int e = -1;
    for (int i = 0; i < 4;i++)
    {
        L.data[i] = a[i];
        L.length += 1;
    }
    printList(L);
    if(ListInsert(L, 3, 5))
        printf("插入成功，插入位序是%d,插入值为%d\n", 3, 5);
    else
        printf("插入失败\n");
    printList(L);
    if(ListDel(L, 5, e))
        printf("删除成功，删除位序是%d,删除值为%d\n", 5, e);
    else
        printf("删除失败\n");
    printList(L);
    printf("%d\n", Listindex(L, 3));
    printf("%d\n", Listval(L, 3));
    printf("%d, %d\n", L.length, L.MaxSize);
    IncreaseSize(L, 5);
    printf("%d, %d", L.length, L.MaxSize);
    return 0;
}

