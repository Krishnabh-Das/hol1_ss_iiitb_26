#include <fcntl.h>
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
int main(void)
{
    int fd = open("fork_output.txt", O_CREAT | O_WRONLY | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open");
        return 1;
    }
    pid_t p = fork();
    if (p < 0)
        return 1;
    if (p == 0) {
        write(fd, "Child writes\\n", 13);
        close(fd);
        return 0;
    }
    write(fd, "Parent writes\\n", 14);
    wait(NULL);
    close(fd);
    return 0;
}
