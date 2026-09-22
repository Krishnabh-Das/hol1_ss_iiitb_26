#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s file\\n", argv[0]);
        return 1;
    }
    int fd = open(argv[1], O_RDWR);
    if (fd == -1) {
        perror("open");
        return 1;
    }
    int flags = fcntl(fd, F_GETFL);
    if (flags == -1) {
        perror("fcntl");
        return 1;
    }
    switch (flags & O_ACCMODE) {
        case O_RDONLY:
            puts("Read only");
            break;
        case O_WRONLY:
            puts("Write only");
            break;
        case O_RDWR:
            puts("Read write");
            break;
    }
    close(fd);
    return 0;
}