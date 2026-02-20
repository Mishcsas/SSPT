#include <bits/stdc++.h>

using namespace std;
    
int main() {
    long long a, b, c;
    cin >> a >> b >> c;
    long long d = b * b - (4 * a * c);
    if (d == 0) {
        cout << -b / (2 * a) << endl;
    } else if (d > 0) {
        d = sqrt(d);
        cout << min((-b - d) / (2 * a), (-b + d) / (2 * a))  << " " << max((-b + d) / (2 * a), (-b - d) / (2 * a)) << endl;
    } else {
        cout << "Нет корней" << endl;
    }
}
