#include <stdio.h>

// 1. コールバック関数として呼び出される関数を定義
int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }

// 2. 関数ポインタを引数にとるメイン関数（計算実行部）
// 引数に「int型の引数を2つとり、int型を返す関数」のアドレスを受け取る
void calculate(int x, int y, int (*callback)(int, int)) {
    int result = callback(x, y); // 受け取った関数を実行
    printf("計算結果: %d\n", result);
}

int main() {
    int a = 10, b = 5;
    
    // 足し算の関数ポインタ（add）を渡して実行
    calculate(a, b, add);
    
    // 引き算の関数ポインタ（subtract）を渡して実行
    calculate(a, b, subtract);
    
    return 0;
}
