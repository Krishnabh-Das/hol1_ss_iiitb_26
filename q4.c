#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(void)
{
    int fd = open("existing.txt", O_RDWR);
    if (fd == -1) {
        perror("open O_RDWR");
        return 1;
    }
    printf("Opened existing.txt with fd=%d\\n", fd);
    close(fd);

    fd = open("existing.txt", O_RDWR | O_CREAT | O_EXCL, 0644);
    if (fd == -1)
        perror("O_EXCL (expected failure if file exists)");
    else {
        printf("Created exclusively, fd=%d\\n", fd);
        close(fd);
    }
    return 0;
}
