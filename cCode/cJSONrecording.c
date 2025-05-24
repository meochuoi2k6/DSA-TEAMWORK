//******************************************************************************************************//
//File này dùng để xử lý các file định dạng JSON dùng trong dự án, bao gồm các hàm:
//  - load_Project_from_json: Load dữ liệu từ file JSON vào struct Project
//  - load_Member_from_json: Load dữ liệu từ file JSON vào struct Member
//  - save_Project_to_json: Lưu dữ liệu từ struct Project vào file JSON
//  - save_Member_to_json: Lưu dữ liệu từ struct Member vào file JSON
//
//
//******************************************************************************************************//






#include "cJSON.h"
#include "struct.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>



#define JSON_MEMBER_FILE "../data/member.json"
#define JSON_PROJECT_FILE "../data/project.json"

//Xử lí file JSON, load dữ liệu từ file JSON vào struct
int load_Project_from_json (cJSON **root) {
    FILE *file = fopen(JSON_PROJECT_FILE, "r");
    if (!file) {
        *root = cJSON_CreateArray();
        return 0;
    }
    fseek(file, 0, SEEK_END);
    long len = ftell(file);
    rewind(file);

    char *data = (char *)malloc(len + 1);
    fread(data, 1, len, file);
    data[len] = '\0';
    fclose(file);


    *root = cJSON_Parse(data);
    free(data);

    if (!*root) {
        *root = cJSON_CreateArray();
        return 0;
    }
    return cJSON_GetArraySize(*root);
}

int is_duplicated_id (cJSON *root, const char *id) {
    int size = cJSON_GetArraySize(root);
    for (int i = 0; i < size; i++) {
        cJSON *curr = cJSON_GetArrayItem(root, i);
        cJSON *id = cJSON_GetObjectItem(curr, "id");
        if (id && strcmp(id->valueint, id) == 0) {
            return 1; // ID đã tồn tại
        }
    }
    return 0; //UNIQUE ID
}










// void save_member_to_json(const char *filename, Node *head) {
//     cJSON *json_array = cJSON_CreateArray();


//     Node *curr = head;
//     while (curr != NULL) {
//         cJSON *json_member = cJSON_CreateObject();
//         cJSON_AddNumberToObject(json_member, "id", curr->data.id);
//         cJSON_AddNumberToObject(json_member, "phoneNumber", curr->data.phoneNumber);
//         cJSON_AddStringToObject(json_member, "name", curr->data.name);
//         cJSON_AddNumberToObject(json_member, "age", curr->data.age);
//         cJSON_AddStringToObject(json_member, "address", curr->data.address);
//         cJSON_AddStringToObject(json_member, "email", curr->data.email);

//         cJSON_AddItemToArray(json_array, json_member);

//         curr = curr->next;
//     }
//     char *json_str = cJSON_Print(json_array);
//     FILE *file = fopen(filename, "w");
//      if (file == NULL) {
//         perror("Error opening file to write JSON");
//         cJSON_Delete(json_array);
//         free(json_str);
//         return;
//     }
//     fprintf(file, "%s", json_str);
//     fclose(file);

//     // Release memory
//     free(json_str);
//     cJSON_Delete(json_array);

//     printf("Data saved to %s\n", filename);

// }



//Check Credential
int is_leap_year (int year) {   //Check năm nhuận
        return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
    }
int valid_date (const char *date) {
    if (strlen(date) != 10) {
        return 0; // Luôn là 10 ký tự
    }
    if (date[2] != '/' || date[5] != '/') {
        return 0; // Phải có định dạng dd/mm/yyyy
    }
    char day_str[3], month_str[3], year_str[5];
    strncpy(day_str, date, 2);
    day_str[2] = '\0';
    strncpy(month_str, date + 3, 2);
    month_str[2] = '\0';
    strncpy(year_str, date + 6, 4);
    year_str[4] = '\0';

    // Kiểm tra toàn bộ là số
    for (int i = 0; i < 2; ++i) {
        if (!isdigit(day_str[i]) || !isdigit(month_str[i])) return 0;
    }
    for (int i = 0; i < 4; ++i) {
        if (!isdigit(year_str[i])) return 0;
    }


    int day = atoi(day_str);
    int month = atoi(month_str);
    if (month < 1 || month > 12) {
        return 0; // Tháng không hợp lệ
    }
    int year = atoi(year_str);

    int max_days_each_month[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (is_leap_year(year)) max_days_each_month[1] = 29;

    // Kiểm tra ngày hợp lệ
    if (day < 1 || day > max_days_each_month[month - 1]) return 0;

    return 1; // Ngày hợp lệ
}




Project Register_a_Project () {
    Project project;
    printf("Enter project name: ");
    fgets(project.name, 50, stdin);
    strip_newline(project.name);

    printf("Enter project ID: ");
    fgets(project.projectID, 10, stdin);
    strip_newline(project.projectID);

    printf("Enter project description: ");
    fgets(project.description, 200, stdin);
    strip_newline(project.description);


    printf("Enter start date (YYYY-MM-DD): ");
    do {
        fgets(project.startDate, 20, stdin);
        strip_newline(project.startDate);
    } while (valid_date(project.startDate));
    printf("Enter end date (YYYY-MM-DD): ");
    do {
        fgets(project.endDate, 20, stdin);
        strip_newline(project.endDate);
    } while (valid_date(project.endDate));
    project.status = 0; // Mặc định là pending mỗi lần tạotạo

    return project;
}