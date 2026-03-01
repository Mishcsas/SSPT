#include <bits/stdc++.h>

using namespace std;
    

bool is_prime(int n) {
    for (int i = 2; i * i < n; i++) {
        if (n % i == 0) {
            return 0;
        }
    }
    return 1;
}


int main() {
    int q, mx = 0;
    cin >> q;
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int x;
            cin >> x;
            if (is_prime(x) && x > mx) {
                mx = x;
            }
        } else {
            if (mx == 0) {
                cout << "Not prime" << endl;
            } else {
                cout << mx << endl;
            }
        }
    }
}
