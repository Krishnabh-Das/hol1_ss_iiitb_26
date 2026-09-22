#include <stdio.h>
#include <unistd.h>
int main(void)
{
    if (link("original.txt", "hard_link_syscall") == -1) {
        perror("link");
        return 1;
    }
    printf("Hard link created.\\n");
    return 0;
}
