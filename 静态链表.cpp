#include <stdio.h>
#define MaxSize 10
typedef struct
{
    int val;
    int next;
} SLinkList[MaxSize];

void InitSLinkList(SLinkList &L)
{
    L[0].next = -1;
    for (int i = 1; i < MaxSize; i++)
        L[i].next = -2;
}

void list_tialinsert(SLinkList &L)
{
    int val, index;
    int tail = 0;
    scanf("%d", &index);
    while(index < 10)
    {
        scanf("%d", &val);
        L[index].val = val;
        L[tail].next = index;
        tail = index;
        scanf("%d", &index);
    }
    L[tail].next = -1;
}

void list_headinsert(SLinkList &L)
{
    int val, index;
    scanf("%d", &index);
    while(index < 10)
    {
        scanf("%d", &val);
        L[index].val = val;
        L[index].next = L[0].next;
        L[0].next = index;
        scanf("%d", &index);
    }
}

bool list_insert(SLinkList &L, int i, int e)
{
    int insert_index = -1;
    int index = 0;
    int j = 0;
    while(L[index].next != -2)
        index++;
    if(index >= 10)
        return false;
    insert_index = index;
    index = 0;
    while(L[index].next != -2 && j < i-1)
    {
        index = L[index].next;
        j++;
    }
    if(L[index].next == -2)
        return false;
    L[insert_index].val = e;
    L[insert_index].next = L[index].next;
    L[index].next = insert_index;
    return true;
}

bool list_delete(SLinkList &L, int i, int &e)
{
    int index = 0;
    int j = 0;
    while(L[index].next != -2 && j < i-1)
    {
        index = L[index].next;
        j++;
    }
    if(L[index].next == -2)
        return false;
    int delete_node = L[index].next;
    L[index].next = L[delete_node].next;
    L[delete_node].next = -2;
    e = L[delete_node].val;
    return true;
}

void print_list(SLinkList L)
{
    int index = 0;
    while(L[index].next != -1)
    {
        index = L[index].next;
        printf("%d->", L[index].val);
    }
    printf("\n");
}

int main()
{
    SLinkList L;
    InitSLinkList(L);
    printf("%d\n", L[9].next);
    list_tialinsert(L);
    // list_headinsert(L);
    if(list_insert(L, 3, 999))
        print_list(L);
    else
        printf("插入失败\n");
    int delete_val = -999;
    if(list_delete(L, 3, delete_val))
    {
        printf("删除值是%d\n", delete_val);
        print_list(L);
    }
    else
        printf("删除失败\n");
    return 0;
}