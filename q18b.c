#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#define SZ 64
int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s record(0-2)\n", argv[0]);
        return 1;
    }
    int r = atoi(argv[1]);
    if (r < 0 || r > 2)
        return 1;
    int fd = open("records.dat", O_RDONLY);
    if (fd < 0) {
        perror("open");
        return 1;
    }
    struct flock f = {
        .l_type = F_RDLCK, .l_whence = SEEK_SET, .l_start = (off_t)r * SZ, .l_len = SZ};
    if (fcntl(fd, F_SETLKW, &f) < 0) {
        perror("lock");
        return 1;
    }
    char b[SZ + 1] = {0};
    pread(fd, b, SZ, (off_t)r * SZ);
    printf("Record %d: %s\n", r, b);
    f.l_type = F_UNLCK;
    fcntl(fd, F_SETLK, &f);
    close(fd);
    return 0;
}
