#include <stdio.h>
#define maxsize 10
// 操作受限的线性表，队尾插入元素，队首删除元素
// 使用取余操作，是有限的空间映射成环形空间
typedef struct{
    int data[maxsize];
    int front, rear;
} SqQueue;

void init_queue(SqQueue &Q)
{
    Q.front = Q.rear = 0;
}

bool queue_empty(SqQueue Q)
{
    if(Q.front == Q.rear)
        return true;
    else
        return false;
}

bool insert_queue(SqQueue &Q, int x)
{
    if((Q.rear+1)%maxsize == Q.front)
        return false;
    Q.data[Q.rear] = x;
    Q.rear = (Q.rear + 1) % maxsize;
    return true;
}

bool delete_queue(SqQueue &Q, int &x)
{
    if(Q.front == Q.rear)
        return false;
    x = Q.data[Q.front];
    Q.front = (Q.front + 1) % maxsize;
    return true;
}

bool get_head(SqQueue Q, int &x)
{
    if(Q.front == Q.rear)
        return false;
    x = Q.data[Q.front];
    return true;
}

void print_queue(SqQueue Q)
{
    for (int i = Q.front; i < Q.rear; i++)
        printf("%d->", Q.data[i]);
    printf("\n");
}

int main()
{
    SqQueue Q;
    init_queue(Q);
    if(queue_empty(Q))
        printf("是空表\n");
    else
        printf("不是空表\n");
    int insert_val;
    scanf("%d", &insert_val);
    while(insert_val != 999  && insert_queue(Q,insert_val))
    {
        scanf("%d", &insert_val);
    }
    print_queue(Q);
    int delete_val = 999;
    if(delete_queue(Q, delete_val))
        printf("出队成功，队首元素是%d\n", delete_val);
    else
        printf("出队失败");
    print_queue(Q);
    int top_val = 999;
    if(get_head(Q, top_val))
        printf("队首元素是%d\n", top_val);
    else
        printf("是空表\n");
    while(Q.front != Q.rear)
    {
        delete_queue(Q, delete_val);
        print_queue(Q);
    }
    if(queue_empty(Q))
        printf("是空表\n");
    else
        printf("不是空表\n");
    return 0;
}
