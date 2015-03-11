/*
*  Author:   huangjunwei@youmi.net
*  Time:     Wed 11 Mar 2015 11:22:47 AM HKT
*  File:     skip_list.c
*  Desc:     my implementation of skip list
*/


#include <iostream>
#include <cmath>
//#include <cstring>
#include <climits>

const int MAX_LEVEL = 6;
const float P = 0.5;

using namespace std;

float frand() {
	return (float) rand() / RAND_MAX;
}

int random_level() {
	static bool first = true;
	if(first) {
		srand((unsigned)time(NULL));
		first = false;
	}

	int lvl = (int)(log(frand()) / log(1.-P));
	return lvl < MAX_LEVEL ? lvl : MAX_LEVEL;
}

struct snode {
	snode *next = nullptr;
	snode *down = nullptr;

	int value = INT_MIN;

	snode(snode *next, snode *down, int value) {
		this->next = next;
		this->down = down;
		this-> value = value;
	}

	~snode() {}
};

struct skiplist {
	snode **headers = nullptr;
	int level = 0;
};

void display(skiplist *list) {
	snode *head = list->headers[0];
	while(nullptr != head) {
		snode *node= head;
		while(nullptr != node) {
			cout << node->value << "->";
			node = node->next;
		}
		cout << endl;
		head = head->down;
	}
}

void init(skiplist *list) {
	list->headers = new snode * [MAX_LEVEL];
	list->level = MAX_LEVEL;


	snode *node1 = new snode(nullptr, nullptr, 1);
	snode *node2 = new snode(nullptr, nullptr, 2);
	snode *node3 = new snode(nullptr, nullptr, 3);
	snode *node4 = new snode(nullptr, nullptr, 1);
	snode *node5 = new snode(nullptr, nullptr, 3);

	node1->next = node2;
	node2->next = node3;
	node4->next = node5;

	node4->down = node1;
	node5->down = node3;

	list->headers = &node4;

	display(list);
}


void insert(skiplist *skiplist, int value) {
	// 随机插入某一层
	int lvl = random_level();
	int i = 0;

	snode *head = skiplist->headers[0];

	// 找到该插入的层
	i = MAX_LEVEL;
	while(--i > lvl) {
		head = head->down;
	}


	cout << head[0]->value << endl;
}


int main() {
	struct skiplist *skiplist = new struct skiplist();
	init(skiplist);

	cout << random_level() << endl;

	return 0;
}
