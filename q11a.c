#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(void)
{
    int fd = open("dup.txt", O_CREAT | O_WRONLY | O_TRUNC | O_APPEND, 0644);
    if (fd == -1) {
        perror("open");
        return 1;
    }
    int d = dup(fd);
    if (d == -1) {
        perror("dup");
        return 1;
    }
    write(fd, "from fd\\n", 8);
    write(d, "from dup\\n", 10);
    close(d);
    close(fd);
    return 0;
}
