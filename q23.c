#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(void)
{
    pid_t p = fork();
    if (p < 0)
        return 1;
    if (p == 0) {
        printf("Child PID=%d exiting.\\n", getpid());
        _exit(0);
    }
    printf("Parent PID=%d, child PID=%d.\\n", getpid(), p);
    printf("Inspect with: ps -l -p %d\\n", p);
    sleep(20);
    return 0;
}
