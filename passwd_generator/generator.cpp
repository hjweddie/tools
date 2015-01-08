/*
*  Author:   huangjunwei@youmi.net
*  Time:     Thu 08 Jan 2015 04:15:33 PM HKT
*  File:     generator.cpp
*  Desc:
*/

#include <iostream>
#include <vector>

using namespace std;

// 33-122
vector<char> digits{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}; // 48-57
vector<char> alphs{'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}; // 97-122
vector<char> calphs{'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}; // 65-90
vector<char> specials{'+', '=', '-', '@', '#', '~', ',', '.', '[', ']', '(', ')', '!', '%', '^', '*', '$'}; // 33-47

string help = "usage: generate [type] -l [length]\ntype:\nd - digits\na - alphabets\nc - capitalized alphabets\ns - specials\n-l	length of the generated password\nexapmple:\ngenerate dacs -l 32\n";

int main(int n, char **args) {
	cout << n;
	if(4 != n) {
		cout << help;
		return 0;
	}

	cout << "hello, world!!" << endl;
	return 0;
}
