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
    L->next = L;//指向自己
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
    r->next = L;
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
    while(r != L)
    {
        printf("%d->", r->val);
        r = r->next;
    }
    printf("\n");
}

int main()
{
    LinkList L;
    InitList(L);
    // List_tailInsert(L);
    List_HeadInsert(L);
    print_list(L);
    return 0;
}