#include <bits/stdc++.h>

using namespace std;
    
int main() {
    long long n, q;
    cin >> n >> q;
    vector<long long> a(n), pref(n + 1, 0);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    for (int i = 1; i <= n; i++) {
        pref[i] = pref[i-1] + a[i-1];
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        l--;
        cout << pref[r] - pref[l] << endl;
    }
}
