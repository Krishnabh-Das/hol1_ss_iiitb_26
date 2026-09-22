#include <stdio.h>
#include <unistd.h>
int main(void)
{
    if (symlink("original.txt", "soft_link_syscall") == -1) {
        perror("symlink");
        return 1;
    }
    printf("Symbolic link created.\\n");
    return 0;
}
