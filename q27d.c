#include <stdio.h>
#include <unistd.h>
int main(void)
{
    {
        char *a[] = {"ls", "-Rl", NULL};
        execv("/bin/ls", a);
    }
    perror("execv");
    return 1;
}
