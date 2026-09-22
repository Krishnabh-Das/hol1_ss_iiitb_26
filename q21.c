#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
int main(void)
{
    pid_t p = fork();
    if (p < 0) {
        perror("fork");
        return 1;
    }
    if (p == 0)
        printf("Child: PID=%d PPID=%d\\n", getpid(), getppid());
    else {
        printf("Parent: PID=%d Child PID=%d\\n", getpid(), p);
        wait(NULL);
    }
    return 0;
}
