#include <stdio.h>
#include <sys/stat.h>
#include <time.h>
int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "Usage: %s file\\n", argv[0]);
        return 1;
    }
    struct stat s;
    if (stat(argv[1], &s) == -1) {
        perror("stat");
        return 1;
    }
    printf("inode: %lu\\n", (unsigned long)s.st_ino);
    printf("hard links: %lu\\n", (unsigned long)s.st_nlink);
    printf("uid: %u\\n", s.st_uid);
    printf("gid: %u\\n", s.st_gid);
    printf("size: %lld bytes\\n", (long long)s.st_size);
    printf("block size: %ld\\n", (long)s.st_blksize);
    printf("blocks: %lld\\n", (long long)s.st_blocks);
    printf("last access: %s", ctime(&s.st_atime));
    printf("last modification: %s", ctime(&s.st_mtime));
    printf("last change: %s", ctime(&s.st_ctime));
    return 0;
}
