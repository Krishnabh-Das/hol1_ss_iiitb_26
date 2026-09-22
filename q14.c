#include <stdio.h>
#include <sys/stat.h>
int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s path\\n", argv[0]);
        return 1;
    }
    struct stat s;
    if (lstat(argv[1], &s) == -1) {
        perror("lstat");
        return 1;
    }
    if (S_ISREG(s.st_mode))
        puts("regular file");
    else if (S_ISDIR(s.st_mode))
        puts("directory");
    else if (S_ISLNK(s.st_mode))
        puts("symbolic link");
    else if (S_ISFIFO(s.st_mode))
        puts("FIFO/named pipe");
    else if (S_ISSOCK(s.st_mode))
        puts("socket");
    else if (S_ISCHR(s.st_mode))
        puts("character device");
    else if (S_ISBLK(s.st_mode))
        puts("block device");
    else
        puts("unknown file type");
    return 0;
}
