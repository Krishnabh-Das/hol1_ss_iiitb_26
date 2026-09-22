#include <stdio.h>
#include <sys/stat.h>
int main(void)
{
    if (mkfifo("my_fifo_syscall", 0666) == -1) {
        perror("mkfifo");
        return 1;
    }
    printf("FIFO created.\\n");
    return 0;
}
