#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(void)
{
    pid_t p = fork();
    if (p < 0)
        return 1;
    if (p > 0) {
        printf("Parent %d exiting; child=%d\\n", getpid(), p);
        return 0;
    }
    sleep(3);
    printf("Child PID=%d, new PPID=%d\\n", getpid(), getppid());
    sleep(5);
    return 0;
}
