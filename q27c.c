#include <stdio.h>
#include <unistd.h>
extern char **environ;
int main(void)
{
    execle("/bin/ls", "ls", "-Rl", (char *)NULL, environ);
    perror("execle");
    return 1;
}
