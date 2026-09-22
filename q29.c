#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
int main(int argc, char **argv)
{
    int p = sched_getscheduler(0);
    if (p < 0) {
        perror("sched_getscheduler");
        return 1;
    }
    printf("Current policy: %s\n", p == SCHED_FIFO    ? "SCHED_FIFO"
                                   : p == SCHED_RR    ? "SCHED_RR"
                                   : p == SCHED_OTHER ? "SCHED_OTHER"
                                                      : "OTHER");
    if (argc < 2)
        return 0;
    int target = (argv[1][0] == 'f') ? SCHED_FIFO : SCHED_RR;
    struct sched_param sp;
    sp.sched_priority = sched_get_priority_min(target);
    if (sched_setscheduler(0, target, &sp) < 0) {
        perror("sched_setscheduler (may require privilege)");
        return 1;
    }
    printf("Changed to %s\n", target == SCHED_FIFO ? "SCHED_FIFO" : "SCHED_RR");
    return 0;
}
