#define _DEFAULT_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>
int main(int argc, char **argv)
{
    if (argc != 3) {
        fprintf(stderr, "Usage: %s HH:MM script.sh\n", argv[0]);
        return 1;
    }
    int hh, mm;
    if (sscanf(argv[1], "%d:%d", &hh, &mm) != 2 || hh < 0 || hh > 23 || mm < 0 || mm > 59)
        return 1;
    pid_t p = fork();
    if (p < 0)
        return 1;
    if (p > 0) {
        printf("Daemon PID=%d\n", p);
        return 0;
    }
    if (setsid() < 0)
        return 1;
    chdir("/");
    umask(0);
    int nullfd = open("/dev/null", O_RDWR);
    dup2(nullfd, 0);
    dup2(nullfd, 1);
    dup2(nullfd, 2);
    close(nullfd);
    while (1) {
        time_t now = time(NULL);
        struct tm t;
        localtime_r(&now, &t);
        if (t.tm_hour == hh && t.tm_min == mm) {
            pid_t c = fork();
            if (c == 0) {
                execl("/bin/sh", "sh", argv[2], (char *)NULL);
                _exit(127);
            }
            if (c > 0)
                waitpid(c, NULL, 0);
            sleep(61);
        }
        sleep(10);
    }
}
