#include <sched.h>
#include <stdio.h>
int main(void)
{
    int max = sched_get_priority_max(SCHED_FIFO);
    int min = sched_get_priority_min(SCHED_FIFO);
    printf("SCHED_FIFO: min=%d max=%d\n", min, max);
    max = sched_get_priority_max(SCHED_RR);
    min = sched_get_priority_min(SCHED_RR);
    printf("SCHED_RR: min=%d max=%d\n", min, max);
    return 0;
}
