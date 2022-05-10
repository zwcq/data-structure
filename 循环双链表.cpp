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
    L->next = L;
    L->prior = L;
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
    r->next = L;
    L->prior = r;//多加一步把头节点的前向指针指向表位
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
        if(L->next != L)//在插入第一个节点后，之后插入节点，得把后一个节点的前向指针指向p，否则所有节点的前向指针都会指向L
            L->next->prior = p;
        else
            L->prior = p;//第一个插入的节点就是尾节点，所以直接在第一步就把L的前向指针指向p
        L->next = p;
        scanf("%d", &x);
    }
}

bool DList_Insert(DLinkList &L, int i, int e)
{
    int j = 1;
    DNode *p, *q;
    p = L->next;//直接从第一个开始找
    if(i < 1)
        return false;
    else if(i == 1)
    {
        q = (DNode *)malloc(sizeof(DNode));
        q->val = e;
        q->next = L->next;
        L->next->prior = q;
        q->prior = L;
        L->next = q;
        return true;
    }
    while(p != L && j < i - 1)
    {
        p = p->next;
        j++;
    }
    if( p == L)
        return false;
    q = (DNode *)malloc(sizeof(DNode));
    q->val = e;
    q->next = p->next;
    //if(p->next != NULL)//循环之后，即使在最后一个节点处后插一个节点，最后一个节点后向指针会指向头节点
    p->next->prior = q;
    q->prior = p;
    p->next = q;
    return true;
}

DNode * get_dnode(DLinkList &L, int i)
{
    int j = 1;
    DNode *p = L->next;
    while (p != L && j < i)
    {
        p = p->next;
        j++;
    }
    if(p == L)
        return NULL;
    else
        return p;
}

DNode * get_val_node(DLinkList &L, int e)
{
    DNode *p = L->next;//怕头节点里有脏数据，最好从第一个节点开始遍历
    while(p != L && p->val != e)
        p = p->next;
    //return p;
    if(p == L)//遍历到最后一位时，p会指向头节点，所以要判断
        return NULL;
    else
        return p;
}

bool insert_nextnode(DNode *p, int e)
{
    DNode *q = (DNode *)malloc(sizeof(DNode));
    if(p == NULL || q == NULL)
        return false;
    q->val = e;
    q->next = p->next;
    // if(p->next != NULL)
    p->next->prior = q;
    q->prior = p;
    p->next = q;
    return true;
}

void prints_dlist(DLinkList &L)
{
    DNode *p = L->next;
    while(p != L)
    {
        printf("%d<->", p->val);
        p = p->next;
    }
    printf("\n");
}

int main()
{
    DLinkList L,L1;
    int delete_val = -999;
    int insert_val = 999;
    if(InitDLinkList(L))
        printf("初始化成功\n");
    else
        printf("初始化失败\n");
    DList_TrailInsert(L);
    // DList_HeadInsert(L);
    prints_dlist(L);
    // if(DList_Insert(L, 1, insert_val))
    //     prints_dlist(L);
    // else
    //     printf("插入失败");
    printf("%d\n", L->prior->val);
    printf("%d\n", get_dnode(L, 3));
    printf("%d\n", get_val_node(L, 3));
    DNode *target = get_dnode(L, 3);
    if(insert_nextnode(target, 999))
        prints_dlist(L);
    else
        printf("插入失败\n");
    return 0;
}