#include <stdio.h>
#define maxsize 10
typedef struct 
{
    int data[maxsize];
    int top;
} sqstack;

void init_sqstack(sqstack &s)
{
    s.top = -1;
}

bool empty_sqstack(sqstack s)
{
    if(s.top == -1)
        return true;
    else
        return false;
}

bool max_sqstack(sqstack s)
{
    if(s.top == maxsize - 1)
        return true;
    else
        return false;
}

bool push(sqstack &s, int x)
{
    if(s.top == maxsize - 1)
        return false;
    s.data[++s.top] = x;
    return true;
}

bool pop(sqstack &s, int &x)
{
    if(s.top == -1)
        return false;
    x = s.data[s.top--];
    return true;
}

bool get_pop(sqstack s, int &x)
{
    if(s.top == -1)
        return false;
    x = s.data[s.top];
    return true;
}

void print_sqstack(sqstack s)
{
    for (int i = 0; i <= s.top; i++)
        printf("%d->", s.data[i]);
    printf("\n");
}

int main()
{
    sqstack s;
    init_sqstack(s);
    printf("%d\n", s.top);
    int x;
    for (int i = 0; i < maxsize; i++)
    {
        scanf("%d", &x);
        push(s, x);
    }
    print_sqstack(s);
    int delete_val;
    if(pop(s, delete_val))
    {
        printf("删除成功，删除值是%d\n", delete_val);
        print_sqstack(s);
    }
    else
        printf("删除失败\n");
    int get_val;
    if(get_pop(s, get_val))
        printf("栈顶元素是%d\n", get_val);
    else
        printf("空栈\n");
    return 0;
}
