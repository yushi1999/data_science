#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#define N 5
#define MAX 1000 //収束最大回数
#define EPS 1.0e-10

bool is_more_than_EPS(double e[N])
{
    int i;

    for (i = 0; i < N; i++)
    {
        if (e[i] <= EPS)
        {
            return false;
        }
    }

    return true;
}

int main(void)
{
    double x[N] = {0.0, 0.0, 0.0};
    double e[N] = {0.0, 0.0, 0.0};
    int i, j, k = 0;
    double a[N][N + 1] = {
        {3.0, 1.0, 0.0, 0.0, 0.0, 7.0},
        {1.0, 2.0, 1.0, 0.0, 0.0, 9.0},
        {0.0, 1.0, 1.0, 1.0, 0.0, 9.0},
        {0.0, 0.0, 1.0, 4.0, 1.0, 21.0},
        {0.0, 0.0, 0.0, 1.0, 5.0, 23.0}};
    double sum, val;

    do
    {
        for (i = 0; i < N; i++)
        {
            sum = 0.0;

            for (j = 0; j < N; j++)
            {
                if (i != j)
                {
                    sum += a[i][j] * x[j];
                }
            }

            val = (1.0 / a[i][i]) * (a[i][N] - sum);
            e[i] = fabs(val - x[i]);
            x[i] = val;
        }
        k++;
    } while (is_more_than_EPS(e));

    //収束回数が最大回数の値だったら正確な解が求まっていない可能性大なので注意
    printf("収束条件: ε< %.10lf\n", EPS);
    printf("収束回数は %d\n", k + 1);
    for (i = 0; i < N; i++)
    {
        printf("x%d = %f\n", i + 1, x[i]);
    }

    return 0;
}