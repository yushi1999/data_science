#include <stdio.h>
#include <math.h>

#define N 5
#define MAX 1000    //最大反復回数
#define EPS 1.0e-10 //収束判定値

// http://pc-physics.com/jacobi1.html

void calc_jacobi(double a[N][N], double b[N], double xnew[N])
{
    int i, j, k;
    double err;
    double xold[N] = {1.0, 1.0, 1.0, 1.0, 1.0};

    for (k = 0; k < MAX; k++)
    {
        err = 0.0; //誤差をリセット
        for (i = 0; i < N; i++)
        {
            xnew[i] = b[i];
            for (j = 0; j < N; j++)
            {
                if (j != i)
                {
                    xnew[i] -= a[i][j] * xold[j];
                }
            }
            xnew[i] /= a[i][i];
        }
        //各解の誤差を足し、古い解は捨て配列xoldに新しい解を入れる
        for (i = 0; i < N; i++)
        {
            err += fabs(xold[i] - xnew[i]); // fabs: double型の絶対値
            xold[i] = xnew[i];
        }

        //足しあわされた誤差が許容範囲内だったら計算終了とし解が求まったとする
        if (err < EPS)
        {
            printf("収束条件: ε< %.10lf\n", EPS);
            printf("収束回数は %d\n", k + 1);
            break;
        }
    }
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
    double x[N];

    calc_jacobi(a, b, x);

    //解の出力
    for (i = 0; i < N; i++)
    {
        printf("x%d = %f\n", i + 1, x[i]);
    }

    return 0;
}
