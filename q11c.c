#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(void)
{
    int fd = open("fcntl_dup.txt", O_CREAT | O_WRONLY | O_TRUNC | O_APPEND, 0644);
    if (fd == -1) {
        perror("open");
        return 1;
    }
    int d = fcntl(fd, F_DUPFD, 100);
    if (d == -1) {
        perror("fcntl");
        return 1;
    }
    write(fd, "from fd\\n", 8);
    write(d, "from fcntl\\n", 12);
    close(d);
    close(fd);
    return 0;
}
