/*
*  Author:   huangjunwei@youmi.net
*  Time:     Wed 11 Mar 2015 11:22:47 AM HKT
*  File:     skip_list.c
*  Desc:     my implementation of skip list
*/

#include <iostream>

using namespace std;


// 链表节点
struct snode {
	snode *next = nullptr;
	snode *down = nullptr;

	int value = INT_MIN;
	int level = 0;

	snode(snode *next, snode *down, int value, int level) {
		this->next = next;
		this->down = down;
		this->value = value;
		this->level = level;
	}

	~snode() {}
};

// 跳跃链表
struct skiplist {
	snode **headers = nullptr;
	const int max_level = 0;

	skiplist(const int &max_level) : max_level(max_level) {
		cout << "max_level: " << max_level << endl;
		this->headers = new snode * [max_level + 1];

		// 初始化每层首节点, 默认第一个节点都是INT_MIN
		this->headers[max_level] = new snode(nullptr, nullptr, INT_MIN, 0);
		for(int i = max_level - 1 ; i > -1; --i) {
			this->headers[i] = new snode(nullptr, headers[i+1], INT_MIN, max_level-i);
		}
	}

	~skiplist() {
		delete [] headers;
	}

	// 图形化形式输出链表
	void display(const skiplist * const list);

	// 检索节点存在
	snode* search(skiplist * const skiplist, const int &value);

	// 删除节点
	bool drop(skiplist * const skiplist, const int &value);

	// 插入节点
	void insert(skiplist * const skiplist, const int &value);
};

