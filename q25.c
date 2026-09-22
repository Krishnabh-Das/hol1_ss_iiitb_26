#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>
int main(void)
{
    pid_t c[3];
    for (int i = 0; i < 3; i++) {
        c[i] = fork();
        if (c[i] < 0)
            return 1;
        if (c[i] == 0) {
            printf("Child %d PID=%d\\n", i + 1, getpid());
            sleep(2 + i);
            _exit(10 + i);
        }
    }
    printf("Waiting specifically for child 2 (PID=%d)\\n", c[1]);
    int st;
    waitpid(c[1], &st, 0);
    if (WIFEXITED(st))
        printf("Child 2 exit status=%d\\n", WEXITSTATUS(st));
    for (int i = 0; i < 3; i++)
        if (c[i] != c[1])
            waitpid(c[i], NULL, 0);
    return 0;
}
