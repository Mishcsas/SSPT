#include <bits/stdc++.h>

using namespace std;
    
int main() {
    int j = 0;
    vector<int> c(3 * 1e8);
    for (int i = 0; i < 3 * 1e8; i++) {
        c[i] = i;
    }
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
}