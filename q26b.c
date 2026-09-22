#include <stdio.h>
#include <unistd.h>
int main(int argc, char **argv)
{
    const char *name = (argc > 1) ? argv[1] : "World";
    execl("/bin/echo", "echo", name, (char *)NULL);
    perror("execl");
    return 1;
}
