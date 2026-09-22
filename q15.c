#include <stdio.h>
extern char **environ;
int main(void)
{
    for (char **p = environ; *p != NULL; ++p)
        puts(*p);
    return 0;
}
