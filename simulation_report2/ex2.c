#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#define N 5
#define MAX 1000    //最大反復回数
#define EPS 1.0e-10 //収束判定値

// https://hiroyukichishiro.com/simultaneous-linear-equations-in-c-language/#i-3

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

void calc_gauss_seidel(double a[N][N], double b[N], double x[N])
{

    double e[N] = {0.0, 0.0, 0.0, 0.0, 0.0};
    double sum, val;
    int i, j, k = 0;

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

            val = (1.0 / a[i][i]) * (b[i] - sum);
            e[i] = fabs(val - x[i]);
            x[i] = val;
        }
        k++;
    } while (is_more_than_EPS(e));

    printf("収束条件: ε< %.10lf\n", EPS);
    printf("収束回数は %d\n", k);
}

int main(void)
{
    int i;
    double a[N][N] = {
        {3.0, 1.0, 0.0, 0.0, 0.0},
        {1.0, 2.0, 1.0, 0.0, 0.0},
        {0.0, 1.0, 1.0, 1.0, 0.0},
        {0.0, 0.0, 1.0, 4.0, 1.0},
        {0.0, 0.0, 0.0, 1.0, 5.0}};
    double b[N] = {7.0, 9.0, 9.0, 21.0, 23.0};
    double x[N] = {1.0, 1.0, 1.0, 1.0, 1.0};

    calc_gauss_seidel(a, b, x);

    //解の出力
    for (i = 0; i < N; i++)
    {
        printf("x%d = %f\n", i + 1, x[i]);
    }

    return 0;
}