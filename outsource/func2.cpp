#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//ĐỊNH NGHĨA STRUCT
// --------- Quan hệ giữa các phần ---------
// 1. Member <-> Task:
//    - Mỗi Task có trường assignedID lưu ID của thành viên đảm nhận công việc.
//    - Cho phép truy xuất thông tin người thực hiện từ Task.
//
// 2. Project <-> Task:
//    - Mỗi Task có trường projectID liên kết tới một Project.
//    - Một Project có thể có nhiều Task, nhưng quan hệ không được lưu ngược lại trong Project.
//
// 3. Task <-> ProgressLog:
//    - Mỗi ProgressLog có taskID để biết nhật ký thuộc về Task nào.
//    - Một Task có thể có nhiều ProgressLog (theo dõi tiến độ).

//CÁC HÀM CHỨC NĂNG
//Member và Project - dùng Cây nhị phân tìm kiếm BST gồm:
/*themTV, themDA: Thêm thành viên mới, Thêm dự án mới vào cây BST theo ID.
timTV, timDA:	Tìm thành viên, Tìm dự án trong cây BST theo ID.
timMinTV, timMinDA:	Tìm thành viên, Tìm dự án có ID nhỏ nhất trong cây BST.
xoaTV, xoaDA:	Xóa thành viên, Xóa dự án theo ID khỏi cây BST.
giaiPhongTV, giaiPhongDA:Giải phóng toàn bộ bộ nhớ cây thành viên, cây dự án.*/

//Task - dùng Danh sách liên kết đơn gồm:
/*themCV	Thêm công việc mới vào đầu danh sách liên kết.
timCV	Tìm công việc theo mã taskID.
xoaCV	Xóa công việc theo mã taskID khỏi danh sách.
giaiPhongCV	Giải phóng toàn bộ danh sách công việc*/

//ProgressLog - dùng Danh sách liên kết đơn gồm:
/*themLog	Thêm nhật ký tiến độ vào đầu danh sách.
xoaLog	Xóa nhật ký theo logID.
giaiPhongLog	Giải phóng toàn bộ danh sách nhật ký tiến độ.*/


// --------- Cau truc du lieu ---------
//Member: Lưu thông tin chi tiết về các thành viên trong hệ thống(BST)




//Project: Quản lý thông tin của các dự án trong hệ thống.(BST)


//Task: Lưu trữ các công việc (task) thuộc về dự án.(DSLK)
typedef struct Task {
    char taskID[10];
    char projectID[10];
    char title[100];
    char description[200];
    char assigneeID[8];
    char dueDate[20];
    int status;  // 0: Todo, 1: In Progress, 2: Done
    struct Task* next;
} Task;

//ProgressLog: Ghi nhận tiến độ thực hiện công việc dưới dạng nhật ký.(DSLK)
typedef struct ProgressLog {
    char logID[10];
    char taskID[10];
    char memberID[8];
    char note[200];
    char timestamp[20];
    struct ProgressLog* next;
} ProgressLog;

// -------------------- Con tro toan cuc --------------------

Task* taskHead = NULL;       
ProgressLog* logHead = NULL; 

// --------- Member (BST) ---------

// Thêm thành viên mới vào cây nhị phân theo ID


// Tìm thành viên theo ID trong cây nhị phân


// Xóa thành viên theo ID khỏi cây nhị phân


// --------- Project (BST) ---------

// Thêm dự án mới vào cây nhị phân theo projectID


// Tìm dự án theo projectID trong cây


// Xóa dự án theo mã khỏi cây nhị phân


// --------- Task (DSLK) ---------

// Thêm công việc mới vào đầu danh sách liên kết đơn
void themCV(Task newTask) {
    Task* t = (Task*)malloc(sizeof(Task));
    *t = newTask;
    t->next = taskHead;
    taskHead = t;
}

// Tìm công việc theo taskID trong danh sách liên kết
Task* timCV(Task* head, const char* id) {
    while (head) {
        if (strcmp(head->taskID, id) == 0) return head;
        head = head->next;
    }
    return NULL;
}

// Xóa công việc theo taskID khỏi danh sách liên kết
void xoaCV(const char* id) {
    Task *curr = taskHead, *prev = NULL;
    while (curr) {
        if (strcmp(curr->taskID, id) == 0) {
            if (prev) prev->next = curr->next;
            else taskHead = curr->next;
            free(curr);
            printf("Da xoa cong viec %s\n", id);
            return;
        }
        prev = curr;
        curr = curr->next;
    }
    printf("Khong tim thay cong viec %s\n", id);
}

// --------- ProgressLog (DSLK) ---------

// Thêm nhật ký tiến độ mới vào đầu danh sách
void themLog(ProgressLog newLog) {
    ProgressLog* l = (ProgressLog*)malloc(sizeof(ProgressLog));
    *l = newLog;
    l->next = logHead;
    logHead = l;
}

// Xóa nhật ký theo logID khỏi danh sách liên kết
void xoaLog(const char* logID) {
    ProgressLog *curr = logHead, *prev = NULL;
    while (curr) {
        if (strcmp(curr->logID, logID) == 0) {
            if (prev) prev->next = curr->next;
            else logHead = curr->next;
            free(curr);
            printf("Da xoa nhat ky %s\n", logID);
            return;
        }
        prev = curr;
        curr = curr->next;
    }
    printf("Khong tim thay nhat ky %s\n", logID);
}

// --------- Giai phong bo nho ---------

// Giải phóng bộ nhớ cây nhị phân thành viên


// Giải phóng bộ nhớ cây nhị phân dự án


// Giải phóng bộ nhớ danh sách công việc
void giaiPhongCV(Task* head) {
    while (head) {
        Task* tmp = head;
        head = head->next;
        free(tmp);
    }
}

// Giải phóng bộ nhớ danh sách nhật ký tiến độ
void giaiPhongLog(ProgressLog* head) {
    while (head) {
        ProgressLog* tmp = head;
        head = head->next;
        free(tmp);
    }
}

// int main() {
//     // Thêm thành viên
//     Member* tv1 = (Member*)malloc(sizeof(Member));
//     tv1->id = 101;
//     strcpy(tv1->name, "Nguyen Van A");
//     strcpy(tv1->role, "Dev");
//     tv1->age = 25;
//     tv1->phoneNumber = 123456789;
//     strcpy(tv1->address, "Hanoi");
//     strcpy(tv1->email, "a@gmail.com");
//     tv1->left = tv1->right = NULL;
//     memberRoot = themTV(memberRoot, tv1);

//     // Thêm dự án
//     Project* da1 = (Project*)malloc(sizeof(Project));
//     strcpy(da1->projectID, "P001");
//     strcpy(da1->name, "Du an 1");
//     strcpy(da1->description, "Mo ta du an 1");
//     strcpy(da1->startDate, "2025-01-01");
//     strcpy(da1->endDate, "2025-06-01");
//     da1->status = 1;
//     da1->left = da1->right = NULL;
//     projectHead = themDA(projectHead, da1);

//     // Thêm công việc
//     Task task1;
//     strcpy(task1.taskID, "T001");
//     strcpy(task1.projectID, "P001");
//     strcpy(task1.title, "Task 1");
//     strcpy(task1.description, "Mo ta task 1");
//     strcpy(task1.assigneeID, "101");
//     strcpy(task1.dueDate, "2025-05-30");
//     task1.status = 0;
//     themCV(task1);

//     // Thêm nhật ký tiến độ
//     ProgressLog log1;
//     strcpy(log1.logID, "L001");
//     strcpy(log1.taskID, "T001");
//     strcpy(log1.memberID, "101");
//     strcpy(log1.note, "Da hoan thanh 50%");
//     strcpy(log1.timestamp, "2025-04-20");
//     themLog(log1);

//     // Tìm thành viên
//     Member* foundMember = timTV(memberRoot, 101);
//     if (foundMember)
//         printf("Tim thay thanh vien: %s\n", foundMember->name);

//     // Tìm dự án
//     Project* foundProject = timDA(projectHead, "P001");
//     if (foundProject)
//         printf("Tim thay du an: %s\n", foundProject->name);

//     // Xóa công việc
//     xoaCV("T001");

//     // Xóa nhật ký
//     xoaLog("L001");

//     // Giải phóng bộ nhớ
//     giaiPhongTV(memberRoot);
//     giaiPhongDA(projectHead);
//     giaiPhongCV(taskHead);
//     giaiPhongLog(logHead);

//     return 0;
// }
