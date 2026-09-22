#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(void)
{
    int fd = creat("created.txt", 0644);
    if (fd == -1) {
        perror("creat");
        return 1;
    }
    printf("File descriptor = %d\\n", fd);
    close(fd);
    return 0;
}
