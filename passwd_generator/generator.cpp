/*
*  Author:   huangjunwei@youmi.net
*  Time:     Thu 08 Jan 2015 04:15:33 PM HKT
*  File:     generator.cpp
*  Desc:
*/

#include <boost/random/mersenne_twister.hpp>
#include <boost/random/discrete_distribution.hpp>
#include <iostream>
#include <unordered_set>
#include <vector>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <string>

using namespace std;

// 33-122
unordered_set<char> digits{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}; // 48-57
unordered_set<char> alphs{'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}; // 97-122
unordered_set<char> calphs{'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}; // 65-90
//unordered_set<char> specials{'+', '=', '-', '@', '#', '~', ',', '.', '[', ']', '(', ')', '!', '%', '^', '*', '$'}; // 33-47
unordered_set<char> specials{'+', '=', '-', '@', '#', '!', '%', '*', '$'};

string help = "usage: generate [type] -l [length]\ntype:\nd - digits\na - alphabets\nc - capitalized alphabets\ns - specials\n-l	length of the generated password\nexapmple:\ngenerate dacs -l 32\n";

int main(int n, char **args) {
	if(4 != n) {
		cout << help;
		return 0;
	}

	// build characters set
	char *types = args[1];
	int types_len = strlen(types), i = -1;
	unordered_set<char> characters;

	while(++i < types_len) {
		switch(*types) {
			case 'd': characters.insert(digits.begin(), digits.end()); break;
			case 'a': characters.insert(alphs.begin(), alphs.end()); break;
			case 'c': characters.insert(calphs.begin(), calphs.end()); break;
			case 's': characters.insert(specials.begin(), specials.end()); break;
			default: cout << "default" << endl;
		}
		++types;
	}

	string result = "";
	int length = atoi(args[3]), csize = characters.size();
	vector<char> chars = vector<char>(characters.begin(), characters.end());

	for(i = 0; i < length; ++i) {
		srand((unsigned)time(0)+i);
		int index = (rand() % csize);
		result = result + chars[index];
	}
	cout << result << endl;
	return 0;
}
