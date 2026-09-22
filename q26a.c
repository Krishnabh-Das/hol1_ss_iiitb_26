#include <stdio.h>
#include <unistd.h>
int main(void)
{
    puts("Before exec");
    execl("/bin/echo", "echo", "Hello from executable", (char *)NULL);
    perror("execl");
    return 1;
}
