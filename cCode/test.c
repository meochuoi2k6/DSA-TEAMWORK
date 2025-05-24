//******************************************************************************************************//
//  Chỉ dùng để test chương trình
//
//
//
//
//
//******************************************************************************************************//





#include "struct.h"
#include "implement.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void checkIfNull (Node *head) {
    if (head == NULL) {
        printf("The list is empty.\n");
    } else {
        printf("The list is not empty.\n");
    }
}

int main () {
    Node *head = NULL;
    Member member1 = {00000001, 912345678, "Alice", 20, "123 Main St", "helloworld@gmail.com"};
    Member member2 = {00000002, 912344128, "Bob", 20, "16 Main St", "helloworld1@gmail.com"};
    sayHelloWorld();
    insertNode(&head, member1);
    insertNode(&head, member2);
    checkIfNull(head);
    displayList(head);
    system("pause");
    return 0;
}