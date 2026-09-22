#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s file\n", argv[0]);
        return 1;
    }

    int fd = open(argv[1], O_RDWR);

    if (fd < 0) {
        perror("open");
        return 1;
    }

    struct flock fl = {
        .l_type = F_WRLCK,
        .l_whence = SEEK_SET,
        .l_start = 0,
        .l_len = 0
    };

    if (fcntl(fd, F_SETLKW, &fl) < 0) {
        perror("fcntl");
        close(fd);
        return 1;
    }

    lseek(fd, 0, SEEK_SET);

    char buf[32] = {0};
    ssize_t n = read(fd, buf, sizeof(buf) - 1);

    if (n < 0) {
        perror("read");
        return 1;
    }

    int ticket = atoi(buf);
    ticket++;

    lseek(fd, 0, SEEK_SET);

    char out[32];
    int len = snprintf(out, sizeof(out), "%d\n", ticket);

    if (write(fd, out, len) != len) {
        perror("write");
        return 1;
    }

    ftruncate(fd, len);

    printf("New ticket number: %d\n", ticket);

    fl.l_type = F_UNLCK;

    if (fcntl(fd, F_SETLK, &fl) < 0)
        perror("unlock");

    close(fd);

    return 0;
}