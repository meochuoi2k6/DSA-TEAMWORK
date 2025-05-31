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

    char buffer[32];
    long line2_pos = 0;
    int line_number = 0;

    while (fgets(buffer, sizeof(buffer), f) != NULL) {
        line_number++;
        if (line_number == 2) {
            line2_pos = ftell(f) - strlen(buffer);
            break;
        }
    }

    if (line_number < 2) {
        fclose(f);
        fprintf(stderr, "File không có đủ 2 dòng\n");
        return NULL;
    }

    size_t pos = strcspn(buffer, "\r\n");
    buffer[pos] = '\0';

    char *original = malloc(strlen(buffer) + 1);
    if (original == NULL) {
        fclose(f);
        fprintf(stderr, "Không đủ bộ nhớ\n");
        return NULL;
    }
    strcpy(original, buffer);

    uint64_t val = strtoull(buffer, NULL, 10);
    val += 1;  // 🔧 Sửa ở đây

    fseek(f, line2_pos, SEEK_SET);
    fprintf(f, "%09" PRIu64 "\n", val);
    fclose(f);

    return original;
}


// ...existing code...

Project create_project(const char* creator, const char *name, const char *desc) {
    Project project;
    memset(&project, 0, sizeof(Project));  // Đảm bảo struct không chứa dữ liệu rác

    // Gán các trường cơ bản
    strncpy(project.name, name, sizeof(project.name) - 1);
    strncpy(project.description, desc, sizeof(project.description) - 1);
    project.description[sizeof(project.description) - 1] = '\0'; // Đảm bảo kết thúc chuỗi
    strncpy(project.ownerID, creator, sizeof(project.ownerID) - 1);
    project.ownerID[sizeof(project.ownerID) - 1] = '\0';
    project.status = 0;

    // Lấy project ID
    char *id = get_next_project_id(PATH_TO_LASTEST_ID);
    if (id == NULL) {
        fprintf(stderr, "Lỗi: Không thể tạo project ID.\n");
        exit(EXIT_FAILURE);  // Hoặc có thể trả về project trống tuỳ cách bạn muốn xử lý
    }

    // Gán ID một cách an toàn
    snprintf(project.projectID, sizeof(project.projectID), "%s", id);
    free(id);

    // TODO: save_Project_to_json(project);

    return project;
}








// Testinggggg

int main () {
    
    Project p = create_project("creator123", "New Project", "This is a new project description.");
    char* d = p.projectID;
    printf("Project ID: %s\n", d);
}