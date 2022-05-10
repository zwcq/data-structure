#include <stdio.h>
#include <stdlib.h>
typedef struct LinkNode
{
    int val;
    struct LinkNode *next;
} LinkNode, *LinkList;

bool InitList(LinkList &L)
{
    L = (LinkNode *) malloc(sizeof(LinkNode));
    if(L == NULL)
        return false;
    L->next = NULL;
    return true;
}

void List_tailInsert(LinkList &L)
{
    int x;
    LinkNode *s, *r;
    r = L;
    scanf("%d",&x);
    while(x!=999)
    {
        s = (LinkNode *)malloc(sizeof(LinkNode));
        s->val = x;
        r->next = s;
        r = s;
        scanf("%d", &x);
    }
    r->next = NULL;
}

void List_HeadInsert(LinkList &L)
{
    int x;
    LinkNode *s;
    // if(L->next == NULL)
    //     printf("yes\n");
    // printf("%d\n", L->next);
    scanf("%d",&x);
    while(x!=999)
    {
        s = (LinkNode *)malloc(sizeof(LinkNode));
        s->val = x;
        s->next = L->next;
        // printf("%d,%d\n", s->val,s->next);
        L->next = s;
        scanf("%d", &x);
    }
}

void print_list(LinkList &L)
{
    LinkNode *r;
    r = L->next;
    while(r != NULL)
    {
        printf("%d->", r->val);
        r = r->next;
    }
    printf("\n");
}

bool ListInsert(LinkList &L, int i, int e)//插入一个新元素到第i位
{
    int j = 0;
    LinkNode *r, *s;
    r = L;
    if(i < 1)
        return false;
    printf("%d\n",i);
    while(r != NULL && j < i - 1)//注意c语言的逻辑运算符
    {
        r = r->next;
        j++;
    }
    printf("%d\n", j);
    if(r == NULL)
        return false;
    s = (LinkNode *)malloc(sizeof(LinkNode));
    s->val = e;
    s->next = r->next;
    r->next = s;
    return true;
}

LinkNode * get_node(LinkList &L, int i)//得到指定节点的地址
{
    int j = 1;
    LinkNode *r;
    if(i < 1)
        return NULL;
    r = L->next;
    while(r != NULL && j < i)
    {
        r = r->next;
        j++;
    }
    return r;
}

bool InsertNextNode(LinkNode *p, int e)
{
    LinkNode *s;
    if(p == NULL)
        return false;
    s = (LinkNode *)malloc(sizeof(LinkNode));
    if(s == NULL)
        return false;
    s->val = e;
    s->next = p->next;
    p->next = s;
    return true;
}

bool InsertPriorNode(LinkNode *p, int e)//时间复杂度为O（1），思路是在指定节点处后插一个节点，复制指定节点的值，再把指定节点的值改为要插入的值；否则从头节点遍历到指定节点，时间复杂度为O（n）
{
    LinkNode *s;
    if(p == NULL)
        return false;
    s = (LinkNode *)malloc(sizeof(LinkNode));
    if(s == NULL)
        return false;
    s->val = p->val;
    s->next = p->next;
    p->val = e;
    p->next = s;
    return true;
}

bool ListDelete(LinkList &L, int i, int &e)
{
    LinkNode *r,*q;
    int j = 0;
    if(i < 1)
        return false;
    r = L;
    while(r != NULL && j < i-1)
    {
        r = r->next;
        j++;
    }    
    if(r == NULL || r->next ==NULL)
        return false;
    q = r->next;
    // printf("%d,%d\n", r->next->next, q->next);
    r->next = q->next;
    e = q->val;
    free(q);
    //这样写容易出问题，r->next已经刷新，e的值会取错，free函数free的对象也是错的，所以要用一个指针指向删除的节点
    // r->next = r->next->next;
    // e = r->next->val;
    // free(r->next);
    return true;
}

bool DeleteNode(LinkList &L, LinkNode *p) //不用从头节点遍历到指定节点，时间复杂度从O(n)到了O(1);核心思路是将指定节点的后一个节点的值覆盖掉指定节点，在free掉指定节点的后一个节点
{
    LinkNode *q = p->next;
    LinkNode *r = L;
    if(p == NULL)
        return false;
    if(q == NULL)//考虑p可能会指向最后一个节点
    {
        while(r->next != p)
            r = r->next;
        r->next = NULL;
        free(p);
    }
    else
    {
        p->val = q->val;//存在问题，当指定节点为最后一个节点时，q指向NULL，这一句会出错。这种情况只能从表头遍历到指定节点
        p->next = q->next;
        free(q);
    }
    
    return true;
}

LinkNode * get_val_node(LinkList &L, int e)
{
    LinkNode *p = L->next;
    while( p != NULL && p->val != e)
        p = p->next;
    return p;
}

LinkList list_reverse(LinkList &L)//空间复杂度为o（n），新建了一个链表
{
    LinkNode *p, *r, *q;
    p = L->next;
    r = (LinkNode *)malloc(sizeof(LinkNode));
    r->next = NULL;
    while(p != NULL)
    {
        q = (LinkNode *)malloc(sizeof(LinkNode));
        q->val = p->val;
        q->next = r->next;
        r->next = q;
        p = p->next;
    }
    return r;
}

void list_reverse1(LinkList &L)//原地逆置。空间复杂度为o（1）
{
    LinkNode *p, *q;
    p = L->next;
    q = p->next;
    while(q != NULL)
    {
        p->next = q->next;
        q->next = L->next;
        L->next = q;
        q = p->next;
    }
}


void reverse_print(LinkList L)//递归的方式，逆序输出，没有改变原有链表结构
{
    if(L->next == NULL)
    {
        printf("%d->", L->val);
        return;
    }
    else
        reverse_print(L->next);
    printf("%d->", L->val);
}


int ListLen(LinkList L)
{
    int l = 0;
    LinkNode *p = L;
    while(p->next != NULL)//判断下一节点是否为空。如果用p！=null来结束循环，算的结果会多一个
    {
        p = p->next;
        l++;
    }
    return l;
}

int main()
{
    LinkList L, L1;
    int delete_val = 0;
    if(InitList(L))
        printf("初始化成功\n");
    else
        printf("初始化失败\n");
    List_tailInsert(L);
    print_list(L);
    // List_HeadInsert(L);
    // print_list(L);
    // if(ListInsert(L, 3, 999))
    //     print_list(L);
    // else
    //     printf("插入失败");
    // LinkNode *x = get_node(L, 3);
    // printf("%d\n",x);
    // if(InsertNextNode(x, 999))
    //     print_list(L);
    // else
    //     printf("插入失败");
    // if(InsertPriorNode(x, 999))
    //     print_list(L);
    // else
    //     printf("插入失败");
    // if(ListDelete(L,1,delete_val))
    // {
    //     printf("删除的是%d\n", delete_val);
    //     print_list(L);
    // }
    // else
    //     printf("删除失败");
    // if(DeleteNode(L, x))
    //     print_list(L);
    // else
    //     printf("删除失败");
    // printf("%d\n", get_val_node(L, 3));
    // printf("%d\n", ListLen(L));
    L1 = list_reverse(L);
    print_list(L1);
    list_reverse1(L1);
    print_list(L1);
    reverse_print(L1->next);//传入参数为第一个节点，而不是头节点
    return 0;
}