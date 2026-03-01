#include <bits/stdc++.h>

using namespace std;
    


int main() {
    string s;
    char c;
    cin >> s >> c;
    map<char, int> m;
    for (int i = 0; i < s.size(); i++) {
        m[s[i]]++;
    }
    cout << m[c] << endl;
}
