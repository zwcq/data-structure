#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct bitnode{
    int val;
    struct bitnode *lchild, *rchild;
} bitnode, *bitree;

typedef struct queue{
    bitnode* val[5];
    int front, rear;
} queue;

bitnode *p;
int j = -1;
void set_tree_preorder(bitree &tree, int a[])
{
    j++;
    // printf("第%d次-%d\n", j, a[j]);
    // int i;
    // scanf("%d", &i);
    if(a[j] == 999)
    {
        tree = NULL;
        return;
    }
    else
    {
        tree = (bitree)malloc(sizeof(bitnode));
        tree->val = a[j];
        // printf("%d\n", tree);
    }
    if(j == 5)
        p = tree;
    set_tree_preorder(tree->lchild, a);
    set_tree_preorder(tree->rchild, a);
}

void enqueue(queue &q, bitnode *p)
{
    if((q.rear + 1)%5 != q.front)
    {
        q.val[q.rear] = p;
        q.rear = (q.rear + 1) % 5;
    }
}

void dequeue(queue &q)
{
    if(q.front != q.rear)
        q.front = (q.front + 1) % 5;
}

void print_tree_ceng(bitree tree, queue &q)
{
    int i = 0;
    double t = -3.14;
    enqueue(q, tree);
    // printf("tree->val:%d\n", tree->val);
    while (q.front != q.rear)
    {
        i++;
        t = log2(i + 1);
        bitnode *s = q.val[q.front];
        // printf("%d-%d-%d\n", s->val,q.front,q.rear);
        printf("%d", s->val);
        if(int(t) == t)//满了一层给回车
            printf("\n");
        // for (int i = q.front; i <= q.rear; i++)
        //     printf("%d--", i);
        // printf("\n");
        dequeue(q);
        if(s->lchild != NULL)
            enqueue(q, s->lchild);
        if(s->rchild != NULL)
            enqueue(q, s->rchild);
    }
    if(int(t) != t)//如果最后一层没满，最后给个回车
        printf("\n");
}

void print_tree_preorder(bitree tree)
{
    if(tree != NULL)
    {
        printf("%d--", tree->val);
        print_tree_preorder(tree->lchild);
        print_tree_preorder(tree->rchild);
    }
}

void print_tree_inorder(bitree tree)
{
    if(tree != NULL)
    {
        print_tree_inorder(tree->lchild);
        printf("%d--", tree->val);
        print_tree_inorder(tree->rchild);
    }
}

void print_tree_postorder(bitree tree)
{
    if( tree != NULL)
    {
        print_tree_postorder(tree->lchild);
        print_tree_postorder(tree->rchild);
        printf("%d--", tree->val);
    }
}


bitnode *pre = NULL;
bitnode *fin = NULL;
void visit_pre(bitnode *q)
{
    if(q != p)
        pre = q;
    else 
        fin = pre;
}

void find_inorder_pre(bitree tree)
{
    if(tree != NULL)
    {
        find_inorder_pre(tree->lchild);
        visit_pre(tree);
        find_inorder_pre(tree->rchild);
    }
}

bitnode *pre_p = NULL;
bitnode *fin_p = NULL;
void visit_post(bitnode *q)
{
    if(pre_p == p)
    {
        fin_p = q;
        return;
    }    
    else
    {
        pre_p = q;
        printf("%d-pre_p\n", pre_p->val);
    }
    
}

void find_inorder_post(bitree tree)
{
    if(tree != NULL)
    {
        find_inorder_post(tree->lchild);
        visit_post(tree);
        find_inorder_post(tree->rchild);
    }
}

int main()
{
    bitree tree;
    queue q;
    q.front = q.rear = 0;
    int a[15] = {1, 2, 4, 999, 999, 5, 999, 999, 3, 6, 999, 999, 7, 999, 999};
    set_tree_preorder(tree, a);
    // printf("%dqqq\n", tree);
    // printf("%d-test\n", tree->val);
    // print_tree_ceng(tree, q);
    // print_tree_preorder(tree);
    // printf("\n");
    // print_tree_inorder(tree);
    // printf("\n");
    // print_tree_postorder(tree);
    // printf("\n");
    // printf("%d-%d\n", tree->val, p->val);
    find_inorder_pre(tree);
    printf("%d-%d\n", fin->val, p->val);
    find_inorder_post(tree);
    printf("%d-%d\n", fin_p->val, p->val);
    return 0;
}