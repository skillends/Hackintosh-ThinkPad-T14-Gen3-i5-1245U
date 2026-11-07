// Estima a frequencia real de 1 thread: um laco com 1 ciclo por iteracao.
// Nao usa privilegios nem acessa registradores.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

static double now(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec / 1e9;
}

static void spin(uint64_t n) {
    __asm__ volatile("1: dec %0\n jnz 1b\n" : "+r"(n) : : "cc");
}

static int cmp(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

int main(void) {
    enum { N = 300 };
    static double g[N];
    const uint64_t it = 40000000;  // cerca de 10 ms por amostra
    for (int i = 0; i < N; i++) {
        double t = now();
        spin(it);
        g[i] = it / (now() - t) / 1e9;
    }
    qsort(g, N, sizeof(double), cmp);
    printf("GHz estimado | min %.2f | p10 %.2f | mediana %.2f | p90 %.2f | max %.2f\n",
           g[0], g[N / 10], g[N / 2], g[N * 9 / 10], g[N - 1]);
    int bins[10] = {0};
    for (int i = 0; i < N; i++) {
        int b = (int)(g[i] * 2);
        if (b > 9) b = 9;
        bins[b]++;
    }
    printf("faixas: ");
    for (int b = 0; b < 10; b++) printf("%.1f-%.1f:%d  ", b / 2.0, (b + 1) / 2.0, bins[b]);
    printf("\n");
    return 0;
}
