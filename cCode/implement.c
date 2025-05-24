//******************************************************************************************************//
//File này dùng để triển khai các hàm cấu trúc dữ liệu cần dùng
//Hiện tại, các cấu trúc dữ liệu đang sử dụng ở Project gồm có:
//  - Linked List (Member)
//  - Stack (Member)
//  - memberList (Arrays of Member)
//
//
// Các lỗi có thể tiềm ẩn và code xử lí ngoại lệ:
//  - (101): Không cấp phát được bộ nhớ cho các node trong linked list và stack
//  - (102): Cấu trúc dữ liệu rỗng
//  - (103): Vị trí ngoài ô nhớ cho phép
//
//******************************************************************************************************//
#include <stdio.h>
#include <stdlib.h>
#include "struct.h"
#include "implement.h"


//Các hàm trả về lỗi:
void printError (int errorCode) {
    switch (errorCode) {
        case 101:
            printf("Memory allocation failed\n");
            break;
        case 102:
            printf("Empty data structure\n");
            break;
        case 103:
            printf("Buffer Overflowed\n");
            break;
        default:
            printf("Unknown error\n");
    }
}


//Các hàm của Link ListList
Node *createNode (Member data) {
    Node *newNode = (Node *)malloc(sizeof(Node));
    if (newNode == NULL) {
        printError(101);
        return NULL;
    }
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}
void appendNode (Node **head, Member data) {
    Node *newNode = createNode(data);
    if (newNode == NULL) {
        printError(101);
        return;
    }
    if (*head == NULL) {
        *head = newNode;
    } else {
        Node *current = *head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = newNode;
    }
}
void addNode (Node **head, Member data) {       //Add ở đây nghĩa là thêm vào đầu danh sách
    Node *newNode = createNode(data);
    if (newNode == NULL) {
        printError(101);
        return;
    }
    newNode->next = *head;
    *head = newNode;
}
void insertAtPossition (Node **head, Member data, int position) {
    if (position < 0) {
        printError(103);
        return;
    }
    Node *newNode = createNode(data);
    if (newNode == NULL) {
        printError(101);
        return;
    }
    if (position == 0) {
        newNode->next = *head;
        *head = newNode;
        return;
    }
    Node *current = *head;
    for (int i = 0; i < position - 1 && current != NULL; i++) {
        current = current->next;
    }
    if (current == NULL) {
        printError(103);
        free(newNode);
        return;
    }
    newNode->next = current->next;
    current->next = newNode;
} 
void popNode (Node **head) {
    if (*head == NULL) {
        printError(102);
        return;
    }
    Node *temp = *head;
    *head = (*head)->next;
    free(temp);
}
void deleteNodeAtPosition (Node **head, int position) {
    if (*head == NULL) {
        printError(102);
        return;
    }
    Node *temp = *head;
    if (position == 0) {
        *head = (*head)->next;
        free(temp);
        return;
    }
    for (int i = 0; i < position - 1 && temp != NULL; i++) {
        temp = temp->next;
    }
    if (temp == NULL || temp->next == NULL) {
        printError(103);
        return;
    }
    Node *toDelete = temp->next;
    temp->next = toDelete->next;
    free(toDelete);
}





//Các hàm của Stack
void push (stack **top, Member data) {
    stack *newNode = (stack *)malloc(sizeof(stack));
    if (newNode == NULL) {
        printError(101);
        return;
    }   
    newNode->data = data;
    newNode->next = *top;
    *top = newNode;
}
Member top (stack *root) {
    if (root == NULL) {
        printError(102);
    }
    return root->data;
}
void pop (stack **top) {
    if (*top == NULL) {
        printError(102);
        return;
    }
    stack *temp = *top;
    *top = (*top)->next;
    free(temp);
}
int stackStatus (stack *root) {
    if (root == NULL) {
        return 0; // Stack is empty
    }
    stack *current = root;
    int count = 0;
    while (current) {
        current = current->next;
        count++;
    }
    return count;
}



//Các hàm của memberList
memberList initMemberList() {           //Khai báo mặc định: memberList arr = initMemberList();
    int capacity = 50;          //Mặc định là 50
    memberList arr;
    arr.data = (Member *)malloc(capacity * sizeof(Member));
    arr.size = 0;
    arr.cap = capacity;
    return arr;
}
int isFull (memberList *arr) {
    return arr->size == arr->cap;
}
int isEmpty (memberList *arr) {
    return arr->size == 0;
}
void resizeMemberList (memberList *arr) {
    int newCapacity = arr->cap * 2;         //Gấp đôi canxi, bạn sợ à?
    Member *newData = (Member *)malloc(newCapacity * sizeof(Member));
    if (newData == NULL) {
        printError(101);
        return;
    }           //Cấp phát bộ nhớ mới, bắt lỗi nếu fail
    for (int i = 0; i < arr->size; i++) {
        newData[i] = arr->data[i];
    }
    free(arr->data);
    arr->data = newData;
    arr->cap = newCapacity;
}
void memberListInsert (memberList *arr, Member member, int pos) {
    if (pos < 0 || pos >= arr->cap) {
        printError(103);
        return;
    }
    if (isFull(arr)) resizeMemberList(arr);
    if (pos == arr->size) {
        arr->data[arr->size++] = member;
    }
    else {
    arr->data[pos] = member;
    arr->size++;
    }
}


//Test zone         ĐHS t làm cái này làm gì :)))))
void displayList(Node *head) {
    Node *current = head;
    while (current != NULL) {
        printf("ID: %ld, Phone Number: %ld, Name: %s, Age: %d, Address: %s, Email: %s\n",
               current->data.id,
               current->data.phoneNumber,
               current->data.name,
               current->data.age,
               current->data.address,
               current->data.email);
        current = current->next;
    }
}



