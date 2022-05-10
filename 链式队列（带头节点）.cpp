#include <stdio.h>
#include <stdlib.h>

typedef struct LinkNode{
    int val;
    struct LinkNode *next;
} LinkNode;

typedef struct{
    LinkNode *front, *rear;
} LinkQueue;

void init_queue(LinkQueue &Q)
{
    Q.front = Q.rear = (LinkNode *)malloc(sizeof(LinkNode));
    Q.front->next = NULL;
}

bool is_empty(LinkQueue Q)
{
    if(Q.front == Q.rear)
        return true;
    else
        return false;
}

void en_queue(LinkQueue &Q, int x)
{
    LinkNode *p = (LinkNode *)malloc(sizeof(LinkNode));
    p->val = x;
    p->next = NULL;
    Q.rear->next = p;
    Q.rear = p;
}

bool de_queue(LinkQueue &Q, int &x)
{
    if(Q.front == Q.rear)
        return false;
    LinkNode *p = Q.front->next;
    x = p->val;
    Q.front->next = p->next;
    if(p->next == NULL)//当删除掉最后一个节点后，要把尾指针指向头指针
        Q.rear = Q.front;
    free(p);
    return true;
}

bool get_top(LinkQueue Q, int &x)
{
    if(Q.front == Q.rear)
        return false;
    x = Q.front->next->val;
    return true;
}

void print_queue(LinkQueue Q)
{
    LinkNode *p = Q.front->next;
    while(p != NULL)
    {
        printf("%d->", p->val);
        p = p->next;
    }
    printf("\n");
}

int main()
{
    LinkQueue Q;
    init_queue(Q);
    if(is_empty(Q))
        printf("是空队列\n");
    else
        printf("不是空队列\n");
    int insert_val;
    scanf("%d", &insert_val);
    while(insert_val != 999)
    {
        en_queue(Q, insert_val);
        scanf("%d", &insert_val);
    }
    print_queue(Q);
    int delete_val = 999;
    if(de_queue(Q, delete_val))
    {
        printf("出队值为%d\n", delete_val);
        print_queue(Q);
    }
    else
        printf("出队失败\n");
    int top_val = 999;
    if(get_top(Q, top_val))
        printf("队首元素是%d\n", top_val);
    else
        printf("是空队\n");
    while(Q.front != Q.rear)
    {
        de_queue(Q, delete_val);
        print_queue(Q);
    }
    if(is_empty(Q))
        printf("是空队列\n");
    else
        printf("不是空队列\n");
    return 0;
}