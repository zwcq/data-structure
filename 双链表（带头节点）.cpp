#include <stdio.h>
#include <stdlib.h>

typedef struct DNode
{
    int val;
    struct DNode *prior, *next;
} DNode, *DLinkList;

bool InitDLinkList(DLinkList &L)
{
    L = (DNode *)malloc(sizeof(DNode));
    if(L == NULL)
        return false;
    L->next = NULL;
    L->prior = NULL;
    return true;
}

void DList_TrailInsert(DLinkList &L)
{
    int x;
    DNode *r, *p;
    r = L;
    scanf("%d", &x);
    while(x != 999)
    {
        p = (DNode *)malloc(sizeof(DNode));
        p->val = x;
        r->next = p;
        p->prior = r;
        r = r->next;
        scanf("%d", &x);
    }
    r->next = NULL;
}

void DList_HeadInsert(DLinkList &L)
{
    int x;
    DNode *p;
    scanf("%d", &x);
    while(x != 999)
    {
        p = (DNode *)malloc(sizeof(DNode));
        p->val = x;
        p->prior = L;
        p->next = L->next;
        if(L->next != NULL)//在插入第一个节点后，之后插入节点，得把后一个节点的前向指针指向p，否则所有节点的前向指针都会指向L
            L->next->prior = p;
        L->next = p;
        scanf("%d", &x);
    }
}

bool DList_Insert(DLinkList &L, int i, int e)
{
    int j = 0;
    DNode *p, *q;
    p = L;
    if(i < 1)
        return false;
    while(p != NULL && j < i - 1)
    {
        p = p->next;
        j++;
    }
    if( p == NULL)
        return false;
    q = (DNode *)malloc(sizeof(DNode));
    q->val = e;
    q->next = p->next;
    if(p->next != NULL)
        p->next->prior = q;
    q->prior = p;
    p->next = q;
    return true;
}

DNode * get_dnode(DLinkList &L, int i)
{
    int j = 0;
    DNode *p = L;
    while (p != NULL && j < i)
    {
        p = p->next;
        j++;
    }
    return p;
}

DNode * get_val_node(DLinkList &L, int e)
{
    DNode *p = L->next;//怕头节点里有脏数据，最好从第一个节点开始遍历
    while(p != NULL && p->val != e)
        p = p->next;
    return p;
}

bool insert_nextnode(DNode *p, int e)
{
    DNode *q = (DNode *)malloc(sizeof(DNode));
    if(p == NULL || q == NULL)
        return false;
    q->val = e;
    q->next = p->next;
    if(p->next != NULL)
        p->next->prior = q;
    q->prior = p;
    p->next = q;
    return true;
}

bool insert_priornode(DNode *p, int e)
{
    DNode *q = (DNode *)malloc(sizeof(DNode));
    if(p == NULL || q == NULL || p->prior == NULL)
        return false;
    q->val = e;
    q->prior = p->prior;
    p->prior->next = q;
    q->next = p;
    p->prior = q;
    return true;
}

bool insert_priornode1(DNode *p, int e)
{
    DNode *r = p->prior;
    if(r == NULL)
        return false;
    return insert_nextnode(r, e);
}

bool delete_index_node(DLinkList &L, int i, int &e)
{
    DNode *p = L;
    int j = 0;
    while(p != NULL && j < i)
    {
        p = p->next;
        j++;
    }
    if(p == NULL)
        return false;
    e = p->val;
    DNode *q = p->prior;
    q->next = p->next;
    if(p->next != NULL)
        p->next->prior = q;
    free(p);
    return true;
}

bool delete_node(DNode *p, int &e)
{
    if(p == NULL || p->prior == NULL)//如果p是null的话，就没有p->prior这个值了，p->prior == NULL无法判断，这个函数自然运行不了，而这么写，判断p==null后，直接执行if语句
        return false;//这么写条件判断不好，最好分开来写，或者考虑清楚空指针的情况
    e = p->val;
    DNode *q = p->prior;
    q->next = p->next;
    if(p->next != NULL)
        p->next->prior = q;
    free(p);
    return true;
}

DLinkList dlist_reverse(DLinkList L)
{
    DLinkList L2 = (DNode *)malloc(sizeof(DNode));
    DNode *p = L->next;
    while(p != NULL)
    {
        DNode *q = (DNode *)malloc(sizeof(DNode));
        q->val = p->val;
        q->next = L2->next;
        if(L2->next != NULL)
            L2->next->prior = q;
        q->prior = L2;
        L2->next = q;
        p = p->next;
    }
    return L2;
}

void prints_dlist(DLinkList &L)
{
    DNode *p = L->next;
    while(p != NULL)
    {
        printf("%d<->", p->val);
        p = p->next;
    }
    printf("\n");
}

void printn_dlist(DLinkList &L)
{
    DNode *p = L->next;
    while(p->next != NULL)//把指针移到最后一个节点
        p = p->next;
    while(p != L)
    {
        printf("%d<->", p->val);
        p = p->prior;
    }
    printf("\n");
}

void destory_list(DLinkList &L)
{
    int i = 0;
    while (L->next != NULL)
    {
        delete_node(L->next, i);
        //prints_dlist(L);
    }
    free(L);
    L = NULL;
}

int DListLen(DLinkList &L)
{
    int i = 0;
    DNode *p = L;
    while( p->next != NULL)
    {
        p = p->next;
        i++;
    }
    return i;
}

int main()
{
    DLinkList L,L1;
    int delete_val = -999;
    if(InitDLinkList(L))
        printf("初始化成功\n");
    else
        printf("初始化失败\n");
    DList_TrailInsert(L);
    //DList_HeadInsert(L);
    prints_dlist(L);
    //printn_dlist(L);
    // int insert_val = 999;
    // if(DList_Insert(L, 3, insert_val))
    //     prints_dlist(L);
    // else
    //     printf("插入失败");
    DNode *target = get_dnode(L, 5);
    // printf("%d\n", get_dnode(L, 3));
    // printf("%d\n", get_val_node(L, 3));
    // if(insert_nextnode(target, 999))
    //     prints_dlist(L);
    // else
    //     printf("插入失败\n");
    // if(insert_priornode(target, 999))
    //     prints_dlist(L);
    // else
    //     printf("插入失败\n");
    // if(insert_priornode1(target, 999))
    //     prints_dlist(L);
    // else
    //     printf("插入失败\n");
    // if(delete_index_node(L, 3, delete_val))
    // {
    //     printf("删除值是%d\n", delete_val);
    //     prints_dlist(L);
    // }
    // else
    //     printf("删除失败\n");
    // if(delete_node(target, delete_val))
    // {
    //     printf("删除值是%d\n", delete_val);
    //     prints_dlist(L);
    // }
    // else
    //     printf("删除失败\n");
    // destory_list(L);
    printf("长度是%d\n",DListLen(L));
    L1 = dlist_reverse(L);
    prints_dlist(L1);
    return 0;
}