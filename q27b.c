#include <stdio.h>
#include <unistd.h>
int main(void)
{
    execlp("ls", "ls", "-Rl", (char *)NULL);
    perror("execlp");
    return 1;
}
