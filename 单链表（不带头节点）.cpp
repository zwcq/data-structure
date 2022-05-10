#include <stdio.h>
#include <stdlib.h>
typedef struct LNode
{
    int val;
    LNode *next;
}LNode, *LinkList;

bool InitList(LinkList &L)
{
    L = NULL;
    return true;
}

bool EMPTY(LinkList &L)
{
    if(L == NULL)
        return true;
    else
        return false;
}

void List_TrailInsert(LinkList &L)//不带头节点的，得自己把第一个节点的值写入，不能用循环
{
    int x;
    LNode *s, *r;
    L = (LNode *)malloc(sizeof(LNode));
    scanf("%d", &x);
    L->val = x;
    L->next = NULL;
    r = L;
    scanf("%d", &x);
    while(x!=999)
    {
        s = (LNode *)malloc(sizeof(LNode));
        s->val = x;
        //s->next = NULL;//执行n次
        r->next = s;
        r = s;
        scanf("%d", &x);
    }
    r->next = NULL;//只执行一次
}

void List_HeadInsert(LinkList &L)//得写一个头指针标记，不然第一个会一直在链表第一位
{
    int x;
    LNode *s,*r;
    L = (LNode *)malloc(sizeof(LNode));
    scanf("%d", &x);
    L->val = x;
    L->next = NULL;
    r = L;
    scanf("%d", &x);
    while(x!=999)
    {
        s = (LNode *)malloc(sizeof(LNode));
        s->val = x;
        s->next = r;
        r = s;
        scanf("%d", &x);
    }
    L = r;
}

void print_list(LinkList &L)//没有头节点，直接从第一个节点开始取值
{
    LNode *r;
    r = L;
    while(r != NULL)
    {
        printf("%d->", r->val);
        r = r->next;
    }
    printf("\n");
}

bool ListInsert(LinkList &L, int i, int e)//不带头节点，在第一个位置插入值时，需要手动处理
{
    int j = 1;
    LNode *r, *s;
    if(i < 1)
        return false;
    if(i == 1)
    {
        s = (LNode *)malloc(sizeof(LNode));
        s->val = e;
        s->next = L;
        L = s;
        return true;
    }
    r = L;
    while(r != NULL && j < i-1)
    {
        r = r->next;
        j++;
    }
    if(r == NULL)
        return false;
    s = (LNode *)malloc(sizeof(LNode));
    s->val = e;
    s->next = r->next;
    r->next = s;
    return true;
}

LNode * get_node(LinkList &L, int i)
{
    LNode *p;
    int j = 1;
    if(i<1)
        return NULL;
    p = L;
    while( p != NULL && j < i)
    {
        p = p->next;
        j++;
    }
    return p;
}

bool InsertNextNode(LNode *p, int e)
{
    LNode *r;
    if(p == NULL)
        return false;
    r = (LNode *)malloc(sizeof(LNode));
    if(r == NULL)
        return false;
    r->val = e;
    r->next = p->next;
    p->next = r;
    return true;
}

bool InsertPriorNode(LNode *p, int e)
{
    LNode *r;
    if(p == NULL)
        return false;
    r = (LNode *)malloc(sizeof(LNode));
    if(r == NULL)
        return false;
    r->val = p->val;
    r->next = p->next;
    p->val = e;
    p->next = r;
    return true;
}

bool ListDelete(LinkList &L, int i, int &e)
{
    LNode *p, *q;
    int j = 1;
    if(i < 1)
        return false;
    else if(i == 1)
    {
        q = L;
        L = q->next;
        e = q->val;
        free(q);
        return true;
    }
    p = L;
    while(p != NULL && j < i-1)
    {
        p = p->next;
        j++;
    }
    if(p == NULL || p->next == NULL)
        return false;
    q = p->next;
    p->next = q->next;
    e = q->val;
    free(q);
    return true;
}

bool NodeDelete(LinkList &L, LNode *p, int &e)
{
    LNode *q, *r;
    if(p == NULL)
        return false;
    q = p->next;
    e = p->val;
    if(q == NULL)
    {
        r = L;
        while(r->next != p)
            r = r->next;
        r->next = NULL;
        free(p);
        return true;
    }
    else
    {
        p->val = q->val;
        p->next = q->next;
        free(q);
        return true;
    }
}

LNode * get_val_node(LinkList &L, int e)
{
    LNode *p = L;
    while(p != NULL && p->val != e)
        p = p->next;
    return p;
}

int ListLen(LinkList &L)
{
    LNode *p = L;
    int i = 1;
    while(p->next != NULL)
    {
        p = p->next;
        i++;
    }
    return i;
}

void del_x(LinkList &L, int x)
{
    print_list(L);
    LNode *p;
    if(L == NULL)
        return;
    if(L->val == x)
    {
        p == L;
        L = L->next;//如果被删掉，传进来的L->next被替换成L->next->next
        free(p);
        print_list(L);
        del_x(L, x);
    }
    else
        del_x(L->next, x);//传进来的参数是L->next
    print_list(L);
}

int main()
{
    LinkList L;
    LNode *p;
    int del_val = 0;
    // printf("%d\n", InitList(L));
    // printf("%d\n", EMPTY(L));
    InitList(L);
    List_TrailInsert(L);
    print_list(L);
    del_x(L, 2);
    print_list(L);
    // List_HeadInsert(L);
    // print_list(L);
    // if(ListInsert(L, 3, 999))
    //     print_list(L);
    // else
    //     printf("插入失败");
    // p = get_node(L, 3);
    // printf("%d\n", p);
    // if(InsertNextNode(p, 999))
    //     print_list(L);
    // else
    //     printf("插入失败");
    // if(InsertPriorNode(p, 999))
    //     print_list(L);
    // else
    //     printf("插入失败");
    // if(ListDelete(L, 5, del_val))
    //     {
    //         print_list(L);
    //         printf("%d\n", del_val);
    //     }
    // else
    //     printf("删除失败");
    // if(NodeDelete(L, p, del_val))
    //     {
    //         print_list(L);
    //         printf("%d\n", del_val);
    //     }
    // else
    //     printf("删除失败");
    // printf("%d\n", get_val_node(L, 3));
    // printf("%d\n", ListLen(L));
    return 0;
}