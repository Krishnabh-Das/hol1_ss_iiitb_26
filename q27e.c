#include <stdio.h>
#include <unistd.h>
int main(void)
{
    {
        char *a[] = {"ls", "-Rl", NULL};
        execvp("ls", a);
    }
    perror("execvp");
    return 1;
}
