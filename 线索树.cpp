#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct bitnode{
    int val;
    struct bitnode *lchild, *rchild;
    int ltag, rtag;
} bitnode, *bitree;

bitnode *test;
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
        tree->ltag = tree->rtag = 0;
        // printf("%d\n", tree);
    }
    if(j == 2)
        test = tree;
    set_tree_preorder(tree->lchild, a);
    set_tree_preorder(tree->rchild, a);
}

void inorder(bitree tree)
{
    if(tree != NULL)
    {
        inorder(tree->lchild);
        printf("%d--", tree->val);
        inorder(tree->rchild);
    }
}

bitnode *pre = NULL;
void visit(bitnode *p)
{
    // printf("%d--", p->val);
    if(p->lchild == NULL)
    {
        p->ltag = 1;
        p->lchild = pre;
    }
    if(pre != NULL && pre->rchild == NULL)
    {
        pre->rtag = 1;
        pre->rchild = p;
    }
    pre = p;
}

void inthread(bitree &tree)
{
    if(tree !=NULL)
    {
        inthread(tree->lchild);
        visit(tree);
        inthread(tree->rchild);
    }
}

void creat_inthread(bitree &tree)
{
    pre = NULL;
    if(tree != NULL)
    {
        inthread(tree);
        if(pre->rchild == NULL)//如果最后一个节点无右孩子，直接将rtag置1即可
            pre->rtag = 1;
    }
}

void prethread(bitree &tree)
{
    if(tree != NULL)
    {
        visit(tree);
        // printf("ltag--%d\n", tree->ltag);
        if(tree->ltag == 0)//防止转圈，如果当前根节点没有左孩子，会把lchild指向前向节点，若不判断是线索还是孩子，则会转圈
            prethread(tree->lchild);
        prethread(tree->rchild);
    }
}

void creat_prethread(bitree &tree)
{
    pre = NULL;
    if(tree != NULL)
    {
        prethread(tree);
        if(pre->rchild == NULL)
            pre->rtag = 1;
    }
}

bitnode* find_the_left(bitree tree)//在线索化后，只有当tag==0.才是结点的真正子树
{
    while(tree->lchild != NULL && tree->ltag == 0)
        tree = tree->lchild;
    return tree;
}

bitnode* find_the_right(bitree tree)
{
    while(tree->rchild != NULL && tree->rtag == 0)
        tree = tree->rchild;
    return tree;
}

void inorder_shunxu(bitree tree)//不用遍历，时间复杂度o(n),空间复杂度o(1)
{
    bitnode *p = find_the_left(tree);
    bitnode *last = find_the_right(tree);
    printf("%d--", p->val);
    while(p != last)
    {
        if(p->rtag == 1)
            p = p->rchild; 
        else
            p = find_the_left(p->rchild);
        printf("%d--", p->val);
    }
}

void inorder_nixu(bitree tree)
{
    bitnode *op = find_the_left(tree);
    bitnode *p = find_the_right(tree);
    printf("%d--", p->val);
    while(p != op)
    {
        if(p->ltag == 1)
            p = p->lchild;
        else
            p = find_the_right(p->lchild);
        printf("%d--", p->val);
    }
}

int main()
{
    bitree tree;
    int a[15] = {1, 2, 4, 999, 999, 5, 999, 999, 3, 6, 999, 999, 7, 999, 999};
    set_tree_preorder(tree, a);
    inorder(tree);
    printf("\n");
    creat_inthread(tree);
    printf("val:%d,ltag:%d,ltag:%d\n", test->val,test->ltag, test->rtag);
    // printf("%d--test\n", test->val);
    // printf("test的中序遍历，前向是%d,后向是%d\n", test->lchild->val, test->rchild->val);
    // creat_prethread(tree);
    // printf("test的前序遍历，前向是%d,后向是%d\n", test->lchild->val, test->rchild->val);
    inorder_shunxu(tree);
    printf("\n");
    inorder_nixu(tree);
    printf("\n");
    return 0;
}