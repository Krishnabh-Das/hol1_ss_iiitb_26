#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(void)
{
    int fd = open("sparse.txt", O_CREAT | O_RDWR | O_TRUNC, 0644);
    if (fd == -1) {
        perror("open");
        return 1;
    }
    if (write(fd, "ABCDEFGHIJ", 10) != 10)
        return 1;
    off_t pos = lseek(fd, 10, SEEK_CUR);
    if (pos == (off_t)-1) {
        perror("lseek");
        return 1;
    }
    printf("lseek return value = %lld\\n", (long long)pos);
    if (write(fd, "1234567890", 10) != 10)
        return 1;
    close(fd);
    return 0;
}
