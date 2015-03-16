/*
*  Author:   huangjunwei@youmi.net
*  Time:     Wed 11 Mar 2015 11:22:47 AM HKT
*  File:     skip_list.c
*  Desc:     my implementation of skip list
*/


#include <iostream>
#include <cmath>
#include "skip_list.h"

using namespace std;

int random_level() {
	static bool first = true;
	if(first) {
		srand((unsigned)time(NULL));
		first = false;
	}

	int lvl = (int)(log(frand()) / log(1.-P));
	return lvl < MAX_LEVEL ? lvl : MAX_LEVEL;
}

// 检索节点存在
snode*
skiplist::search(skiplist * const skiplist, const int &value) {
	snode *head = skiplist->headers[0];

	do {
		snode *tnode = head, *pre = head;
		while(nullptr != tnode) {
			if(value == tnode->value) {
				return tnode;
			}

			// 加速层次跳跃
			if(nullptr != tnode->down) {
				head = tnode;
			}

			tnode = tnode->next;
		}
	} while(nullptr != (head = head->down));

	return nullptr;
}

// 删除节点
bool
skiplist::drop(skiplist * const skiplist, const int &value) {
	// 在底层删除节点
	snode *head = skiplist->headers[0];
	while(nullptr != head->down) {
		head = head->down;
	}

	snode *tnode = head;
	while(nullptr != (tnode->next) && value != tnode->next->value) {
		tnode = tnode->next;
	}

	if(nullptr == tnode->next) {
		// 未找到元素
		return false;
	}

	// 找到元素
	snode *dnode = tnode->next; // 将删除节点
	tnode->next = dnode->next;
	delete dnode;

	// 查看有无重复节点
	if(nullptr == tnode->next || value != tnode->next->value) {
		// 无重复节点, 删除上级所有同级索引
		head = skiplist->headers[0];

		while(0 != head->level) {
			snode *node = head;
			while(nullptr != (node->next) && value != node->next->value) {
				node = node->next;
			}

			if(nullptr == node->next) {
				head = head->down;
				continue;
			}

			dnode = node->next;
			node->next = dnode->next;
			delete dnode;

			head = head->down;
		}
	}

	return true;
}

// 插入节点
void
skiplist::insert(skiplist * const skiplist, const int &value) {
	// 随机插入某一层
	int lvl = random_level();
	int i = 0;

	snode *head = skiplist->headers[0];

	//cout << "insert level: " << lvl << endl;
	//cout << "insert value: " << value << endl;

	// 找到该插入的层
	i = skiplist->max_level;
	while(nullptr != head->down && --i > lvl - 1) {
		head = head->down;
	}

	// 插入链表使用的临时变量
	snode *node = nullptr, *up = nullptr;

	// 将value插入该层及以下层
	do {
		// 插入排序，找到该层插入位置
		snode *tnode = head;

		while(nullptr != tnode->next && tnode->next->value < value) {
			tnode = tnode->next;
		}

		if(0 != tnode->level && nullptr != tnode->next && value == tnode->next->value) {
			continue;
		}

		// 在找到的节点tnode后插入
		node = new snode(nullptr, nullptr, value, tnode->level);
		node->next = tnode->next;
		tnode->next = node;

		// 修改上级节点down指针
		if(nullptr != up) {
			up->down = node;
		}
		up = node;
	} while(nullptr != (head = head->down));
}

// 图形化形式输出链表
void
skiplist::display(const skiplist * const list) {
	snode *head = list->headers[0];
	while(nullptr != head) {
		snode *node= head;
		cout << "level " << head->level << ": ";
		while(nullptr != node) {
			cout << node->value;
			if(nullptr != node->down) {
				cout << ".";
			}
			cout << "->";
			node = node->next;
		}
		cout << endl;
		head = head->down;
	}
}

int main() {
	struct skiplist *skiplist = new struct skiplist(6);

	cout << "initial skip list" << endl;
	skiplist->display(skiplist);

	//snode *node1 = new snode(nullptr, nullptr, 1, 0);
	//snode *node2 = new snode(nullptr, nullptr, 2, 0);
	//snode *node3 = new snode(nullptr, nullptr, 3, 0);
	//snode *node4 = new snode(nullptr, nullptr, 1, 1);
	//snode *node5 = new snode(nullptr, nullptr, 3, 1);

	//node1->next = node2;
	//node2->next = node3;
	//node4->next = node5;

	//node4->down = node1;
	//node5->down = node3;

	//skiplist->headers = &node4;

	cout << "before insertion skip list" << endl;
	skiplist->display(skiplist);
	cout << "after insertion skip list" << endl;
	skiplist->insert(skiplist, 4);
	skiplist->insert(skiplist, 1);
	skiplist->display(skiplist);
	//snode *node = skiplist->search(skiplist, 6);
	//cout << "after deletion skip list" << endl;
	//skiplist->drop(skiplist, 4);
	//skiplist->display(skiplist);

	return 0;
}
