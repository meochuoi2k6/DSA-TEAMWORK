//******************************************************************************************************//
//File này dùng để xử lý các file định dạng JSON dùng trong dự án, bao gồm các hàm:
//  - load_Project_from_json: Load dữ liệu từ file JSON vào struct Project
//  - load_Member_from_json: Load dữ liệu từ file JSON vào struct Member
//  - save_Project_to_json: Lưu dữ liệu từ struct Project vào file JSON
//  - save_Member_to_json: Lưu dữ liệu từ struct Member vào file JSON
//
//
//******************************************************************************************************//



#include "struct.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <inttypes.h>
#include <ctype.h>


#define JSON_MEMBER_FILE "../data store/member.json"
#define JSON_PROJECT_FILE "../data store/project.json"
#define PATH_TO_LASTEST_ID "../data store/lastest_id.txt"
//******************************************************************************************************//
//Xử lí file JSON, load dữ liệu từ file JSON vào struct

// ...existing code...

// Sửa hàm get_next_project_id để nhận tham số đường dẫn file
char* get_next_project_id(const char* path) {
    FILE *f = fopen(path, "r+");
    if (f == NULL) {
        perror("Không thể mở file");
        return NULL;
    }

    char buffer[32]; // Đủ chứa dòng + newline + \0
    long line2_pos = 0;
    int line_number = 0;

    // Đọc từng dòng, nhớ vị trí bắt đầu dòng 2
    while (fgets(buffer, sizeof(buffer), f) != NULL) {
        line_number++;
        if (line_number == 2) {
            // Vị trí bắt đầu dòng 2 = vị trí hiện tại trừ độ dài dòng vừa đọc
            line2_pos = ftell(f) - strlen(buffer);
            break;
        }
    }

    if (line_number < 2) {
        fclose(f);
        fprintf(stderr, "File không có đủ 2 dòng\n");
        return NULL;
    }

    // Loại bỏ newline nếu có (cả \r và \n)
    size_t pos = strcspn(buffer, "\r\n");
    buffer[pos] = '\0';  // An toàn vì pos <= strlen(buffer)

    // Sao chép chuỗi gốc (dòng 2) để trả về
    char *original = malloc(strlen(buffer) + 1);
    if (original == NULL) {
        fclose(f);
        fprintf(stderr, "Không đủ bộ nhớ\n");
        return NULL;
    }
    strcpy(original, buffer);

    // Chuyển sang số rồi tăng
    uint64_t val = strtoull(buffer, NULL, 10);
    val += 10;

    // Ghi lại giá trị mới với định dạng 9 chữ số zero-padded + newline
    fseek(f, line2_pos, SEEK_SET);
    fprintf(f, "%09" PRIu64 "\n", val);
    fclose(f);

    return original;
}

// ...existing code...

Project create_project(const char* creator, const char *name, const char *desc) {
    Project project;
    memset(&project, 0, sizeof(Project));  // Đảm bảo không có rác

    strncpy(project.name, name, sizeof(project.name) - 1);
    strncpy(project.description, desc, sizeof(project.description) - 1);
    project.description[sizeof(project.description) - 1] = '\0'; // Đảm bảo chuỗi kết thúc
    strncpy(project.ownerID, creator, sizeof(project.ownerID) - 1);
    project.status = 0;

    char *id = get_next_project_id(PATH_TO_LASTEST_ID);

    strncpy(project.projectID, id, sizeof(project.projectID) - 1);
    free(id);

    // TODO: save_Project_to_json(project);

    return project;
}







// Testinggggg

int main () {
    
    Project project;
    project = create_project("Shiro", "Project A", "This is a test project");
    printf("Project created with ID: %s\n", project.projectID);
    printf("Project Name: %s\n", project.name);
    printf("Project Description: %s\n", project.description);
    printf("Project Owner ID: %s\n", project.ownerID);

}