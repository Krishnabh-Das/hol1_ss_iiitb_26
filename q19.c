#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <x86intrin.h>
int main(void)
{
    const int N = 1000000;
    uint64_t start = __rdtsc();
    for (int i = 0; i < N; i++)
        (void)getpid();
    uint64_t end = __rdtsc();
    printf("Average cycles per getpid: %.2f\\n", (double)(end - start) / N);
    return 0;
}
