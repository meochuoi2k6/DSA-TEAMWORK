// File: cCode/test_id.c
#include <stdio.h>
#include "implement.h" // Import các hàm của chúng ta

int main() {
    printf("Testing get_next_id function...\n");

    // Test lấy ID cho user
    char* user_id = get_next_id("user");
    if (user_id != NULL) {
        printf("Successfully got new user ID: %s\n", user_id);
        free_c_string(user_id); // Nhớ giải phóng bộ nhớ
    } else {
        printf("Failed to get user ID.\n");
    }

    // Test lấy ID cho project
    char* project_id = get_next_id("project");
    if (project_id != NULL) {
        printf("Successfully got new project ID: %s\n", project_id);
        free_c_string(project_id);
    } else {
        printf("Failed to get project ID.\n");
    }

    printf("Test finished.\n");
    return 0;
}