#include <bits/stdc++.h>

using namespace std;

map<long long, long long> fact(long long n) {
    map<long long, long long> res;
    for (long long i = 2; i * i <= n; i++) {
        while (n % i == 0) {
            res[i]++;
            n /= i;
        }
    }
    if (n > 1) {
        res[n]++;
    }
    return res;
}

int main() {
    long long n;
    cin >> n;
    string res = "";
    for (auto [d, c] : fact(n)) {
        for (int i = 0; i < c; i++) {
            res += to_string(d) + '*';
        }
    }
    res.pop_back();
    cout << res << endl;
}
