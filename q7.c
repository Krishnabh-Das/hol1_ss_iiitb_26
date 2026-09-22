#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
int main(int argc, char *argv[])
{
    if (argc != 3) {
        fprintf(stderr, "Usage: %s file1 file2\\n", argv[0]);
        return 1;
    }
    int in = open(argv[1], O_RDONLY);
    if (in == -1) {
        perror("open source");
        return 1;
    }
    int out = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (out == -1) {
        perror("open destination");
        close(in);
        return 1;
    }
    char buf[4096];
    ssize_t n;
    while ((n = read(in, buf, sizeof(buf))) > 0) {
        ssize_t done = 0;
        while (done < n) {
            ssize_t x = write(out, buf + done, (size_t)(n - done));
            if (x <= 0) {
                perror("write");
                return 1;
            }
            done += x;
        }
    }
    close(in);
    close(out);
    return n < 0;
}
