#include <stdio.h>
#include <sys/resource.h>
#include <unistd.h>
int main(void)
{
    int p = getpriority(PRIO_PROCESS, 0);
    printf("PID=%d, nice/priority value=%d\\n", getpid(), p);
    return 0;
}
