#include <bits/stdc++.h>

using namespace std;
    
int main() {
    string a, b;
    cin >> a >> b;
    for (int i = 0; i < a.size(); i++) {
        if (i % 2 == 0 && b[i] == '1') {
            swap(a[i], b[i]);
        } 
        if (i % 2 == 1 && a[i] == '1') {
            swap(a[i], b[i]);
        }
    }
    if (a < b) {
        cout << "Bob" << endl;
    } else if (a > b) {
        cout << "Alice" << endl;
    } else {
        cout << "Draw" << endl;
    }
}
