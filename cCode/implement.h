#ifndef IMPLEMENT_H
#define IMPLEMENT_H
#include <stdio.h>
#include <stdlib.h>
#include "struct.h"


//Error handling functions
void printError (int errorCode);



// Danh sách các hàm của linked listlist
Node* createNode (Member data);
void displayList(Node *head);
void appendNode (Node **head, Member data);
void popNode (Node **head);
void insertAtPossition (Node **head, Member data, int position);
void deleteNodeAtPosition (Node **head, int position);


// Danh sách các hàm của stack
void push(stack **top, Member data);
Member top (stack *root);
void pop(stack **top);
int stackStatus (stack *root);


// Danh sách các hàm của memberList
memberList initMemberList();
int isFull (memberList *arr);
int isEmpty (memberList *arr);
void resizeMemberList (memberList *arr);
void memberListInsert (memberList *arr, Member member, int pos);
#endif