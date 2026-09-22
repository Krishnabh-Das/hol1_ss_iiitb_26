#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(void)
{
    int fd[5];
    char name[32];
    for (int i = 0; i < 5; ++i) {
        snprintf(name, sizeof(name), "q5_file_%d.txt", i + 1);
        fd[i] = open(name, O_CREAT | O_RDWR, 0644);
        if (fd[i] == -1) {
            perror("open");
            return 1;
        }
        printf("fd[%d] = %d\\n", i, fd[i]);
    }
    printf("PID = %d\\n", getpid());
    fflush(stdout);
    while (1)
        sleep(1);
    return 0;
}
