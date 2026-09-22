#include <unistd.h>
int main(void)
{
    char buf[1024];
    ssize_t n;
    while ((n = read(STDIN_FILENO, buf, sizeof(buf))) > 0) {
        ssize_t sent = 0;
        while (sent < n) {
            ssize_t w = write(STDOUT_FILENO, buf + sent, (size_t)(n - sent));
            if (w <= 0)
                return 1;
            sent += w;
        }
    }
    return n < 0;
}
