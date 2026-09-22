#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(void)
{
    int fd = open("dup2.txt", O_CREAT | O_WRONLY | O_TRUNC | O_APPEND, 0644);
    if (fd == -1) {
        perror("open");
        return 1;
    }
    int d = dup2(fd, 100);
    if (d == -1) {
        perror("dup2");
        return 1;
    }
    write(fd, "from fd\\n", 8);
    write(d, "from dup2\\n", 11);
    close(d);
    close(fd);
    return 0;
}
