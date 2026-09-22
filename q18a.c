#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#define SZ 64
static int setlock(int fd, int r, short type)
{
    struct flock f = {.l_type = type, .l_whence = SEEK_SET, .l_start = (off_t)r * SZ, .l_len = SZ};
    return fcntl(fd, F_SETLKW, &f);
}
static void unlock(int fd, int r)
{
    struct flock f = {
        .l_type = F_UNLCK, .l_whence = SEEK_SET, .l_start = (off_t)r * SZ, .l_len = SZ};
    fcntl(fd, F_SETLK, &f);
}
int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s record(0-2)\n", argv[0]);
        return 1;
    }
    int r = atoi(argv[1]);
    if (r < 0 || r > 2)
        return 1;
    int fd = open("records.dat", O_RDWR | O_CREAT, 0644);
    if (fd < 0) {
        perror("open");
        return 1;
    }
    if (setlock(fd, r, F_WRLCK) < 0) {
        perror("lock");
        return 1;
    }
    char b[SZ] = {0};
    snprintf(b, SZ, "Record %d modified by PID %d", r, getpid());
    pwrite(fd, b, SZ, (off_t)r * SZ);
    printf("Modified record %d\n", r);
    unlock(fd, r);
    close(fd);
    return 0;
}
