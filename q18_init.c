#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#define SZ 64
int main(void)
{
    int fd = open("records.dat", O_CREAT | O_RDWR | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open");
        return 1;
    }
    for (int i = 0; i < 3; i++) {
        char b[SZ] = {0};
        snprintf(b, SZ, "Initial record %d", i);
        write(fd, b, SZ);
    }
    close(fd);
    puts("Three records created.");
    return 0;
}
