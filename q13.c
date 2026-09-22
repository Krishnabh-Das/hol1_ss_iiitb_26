#include <stdio.h>
#include <sys/select.h>
#include <unistd.h>
int main(void)
{
    fd_set set;
    FD_ZERO(&set);
    FD_SET(STDIN_FILENO, &set);

    struct timeval tv = {10, 0};
    printf("Waiting for STDIN for 10 seconds...\\n");
    fflush(stdout);
    int r = select(STDIN_FILENO + 1, &set, NULL, NULL, &tv);
    if (r > 0) {
        char buf[256];
        ssize_t n = read(STDIN_FILENO, buf, sizeof(buf) - 1);
        if (n > 0) {
            buf[n] = 0;
            printf("Data available: %s", buf);
        }
    } else if (r == 0)
        puts("No data available within 10 seconds.");
    else
        perror("select");
    return 0;
}
