// File: cCode/implement.h
#ifndef IMPLEMENT_H
#define IMPLEMENT_H

#define EXPORT __declspec(dllexport)

#include "struct.h"

// Hàm quản lý ID
EXPORT char* get_next_id(const char* type);

// Các hàm quản lý Project
EXPORT void create_project(char *name, char *description, char *ownerID, char *startDate, char *endDate, int status, char **memberID, int currentMember);
EXPORT void delete_project_by_id(const char* projectID);

// Các hàm quản lý Task
EXPORT void add_task_to_project(const char* projectID, const char* title, const char* description, const char* assigneeID);
EXPORT void update_task_status(const char* projectID, const char* taskID, const char* newStatus);

// Hàm giải phóng bộ nhớ cho chuỗi
EXPORT void free_c_string(char* str);

#endif // IMPLEMENT_H