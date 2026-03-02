#include <bits/stdc++.h>

using namespace std;
    
long long MOD = 1e9 + 7;

int main() {
    int n;
    cin >> n;
    vector<long long> dp(n + 1, 0);
    dp[1] = 1;
    for (int i = 1; i < n; i++) {
        dp[i + 1] = (dp[i+1] + dp[i]) % MOD;
        if (i * 2 <= n) {
            dp[i * 2] = (dp[i * 2] + dp[i]) % MOD;
        }
    }
    cout << MOD << endl;
    cout << dp[n] << endl;
}
