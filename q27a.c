#include <stdio.h>
#include <unistd.h>
int main(void)
{
    execl("/bin/ls", "ls", "-Rl", (char *)NULL);
    perror("execl");
    return 1;
}
