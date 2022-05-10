#include <stdio.h>
#include <stdlib.h>

typedef struct linknode{
    int val;
    struct linknode *next;
} Lnode, * LiStack;

bool init_listack(LiStack &L)//头指针是头指针，头节点是头节点
{
    L = NULL;
    return true;
}

bool empty_listack(LiStack L)
{
    if(L == NULL)
        return true;
    else
        return false;
}

bool push(LiStack &L, int x)
{
    Lnode *p = (Lnode *)malloc(sizeof(Lnode));
    if(p == NULL)
        return false;
    p->val = x;
    p->next = L;
    L = p;
    return true;
}

bool pop(LiStack &L, int &x)
{
    if(L == NULL)
        return false;
    x = L->val;
    Lnode *q = L;
    L = L->next;
    free(q);
    return true;
}

bool get_pop(LiStack L, int &x)
{
    if(L == NULL)
        return false;
    x = L->val;
    return true;
}

void print_stack(LiStack L)
{
    Lnode *p = L;
    while(p != NULL)
    {
        printf("%d->", p->val);
        p = p->next;
    }
    printf("\n");
}

int main()
{
    LiStack L;
    if(init_listack(L))
        printf("初始化成功\n");
    else
        printf("初始化失败\n");
    if(empty_listack(L))
        printf("是空栈\n");
    else
        printf("不是空栈\n");
    int x;
    scanf("%d", &x);
    while(x != 999)
    {
        push(L, x);
        scanf("%d", &x);
    }
    print_stack(L);
    int delete_val;
    if(pop(L, delete_val))
    {
        printf("删除值是%d\n", delete_val);
        print_stack(L);
    }
    else
        printf("删除失败\n");
    int pop_val;
    if(get_pop(L, pop_val))
        printf("栈顶元素是%d\n", pop_val);
    else
        printf("空栈\n");
    return 0;
}