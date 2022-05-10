#include <stdio.h>
int main()
{
    char a[10] = "abcdefg";
    char *p = a;
    int b = -1;
    int i = 0;
    while(p[i] != NULL)
    {
        printf("%c", p[i]);
        i++;
    }
    return 0;
}