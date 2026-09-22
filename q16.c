#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc != 3) {
        fprintf(stderr, "Usage: %s file r|w\n", argv[0]);
        return 1;
    }

    int fd = open(argv[1], O_RDWR | O_CREAT, 02660);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    if (fchmod(fd, 02660) == -1) {
        perror("fchmod");
        close(fd);
        return 1;
    }

    struct flock fl = {0};

    if (argv[2][0] == 'w')
        fl.l_type = F_WRLCK;
    else if (argv[2][0] == 'r')
        fl.l_type = F_RDLCK;
    else {
        fprintf(stderr, "Use r for read lock or w for write lock\n");
        close(fd);
        return 1;
    }

    fl.l_whence = SEEK_SET;
    fl.l_start = 0;
    fl.l_len = 0;

    printf("Requesting %s lock...\n", fl.l_type == F_WRLCK ? "write" : "read");

    if (fcntl(fd, F_SETLKW, &fl) == -1) {
        perror("fcntl");
        close(fd);
        return 1;
    }

    printf("Lock acquired. Press Enter to release it.\n");
    getchar();

    fl.l_type = F_UNLCK;

    if (fcntl(fd, F_SETLK, &fl) == -1)
        perror("unlock");

    close(fd);

    return 0;
}