// File: cCode/createProject.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "implement.h"
#include "../external/cJSON/cJSON.h"

#define JSON_PROJECT_FILE "data store/project.json"
#define JSON_IDS_FILE "data store/latest_ids.json"

cJSON* load_json_from_file(const char* filepath) {
    FILE* file = fopen(filepath, "r");
    if (file == NULL) return NULL;
    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    fseek(file, 0, SEEK_SET);
    if (length == 0) {
        fclose(file);
        return cJSON_CreateObject();
    }
    char* buffer = (char*)malloc(length + 1);
    if (buffer == NULL) {
        fclose(file);
        return NULL;
    }
    fread(buffer, 1, length, file);
    fclose(file);
    buffer[length] = '\0';
    cJSON* json = cJSON_Parse(buffer);
    free(buffer);
    return json;
}

void write_json_to_file(const char* filepath, cJSON* json) {
    char* json_str = cJSON_Print(json);
    if (json_str != NULL) {
        FILE* file = fopen(filepath, "w");
        if (file != NULL) {
            fprintf(file, "%s\n", json_str);
            fclose(file);
        }
        free(json_str);
    }
}

cJSON* load_all_projects_as_json_array(const char* filepath) {
    cJSON* projects_json = load_json_from_file(filepath);
    if (projects_json == NULL || !cJSON_IsArray(projects_json)) {
        if (projects_json) cJSON_Delete(projects_json);
        return cJSON_CreateArray();
    }
    return projects_json;
}

EXPORT char* get_next_id(const char* type) {
    cJSON* ids_json = load_json_from_file(JSON_IDS_FILE);
    if (ids_json == NULL) { ids_json = cJSON_CreateObject(); }
    cJSON* id_item = cJSON_GetObjectItemCaseSensitive(ids_json, type);
    if (!cJSON_IsNumber(id_item)) {
        cJSON_AddNumberToObject(ids_json, type, 0);
        id_item = cJSON_GetObjectItemCaseSensitive(ids_json, type);
    }
    int current_id = id_item->valueint;
    current_id++;
    cJSON_SetNumberValue(id_item, current_id);
    write_json_to_file(JSON_IDS_FILE, ids_json);
    cJSON_Delete(ids_json);
    char* next_id_str = malloc(sizeof(char) * 15);
    if (next_id_str == NULL) return NULL;
    if (strcmp(type, "project") == 0) { sprintf(next_id_str, "PRJ%09d", current_id); }
    else if (strcmp(type, "task") == 0) { sprintf(next_id_str, "TSK%09d", current_id); }
    else if (strcmp(type, "user") == 0) { sprintf(next_id_str, "USR%09d", current_id); }
    else { sprintf(next_id_str, "ID%09d", current_id); }
    return next_id_str;
}

EXPORT void create_project(char *name, char *description, char *ownerID, char *startDate, char *endDate, int status, char **memberID, int currentMember) {
    cJSON *projects_array = load_all_projects_as_json_array(JSON_PROJECT_FILE);
    cJSON *project_json = cJSON_CreateObject();
    char* new_id = get_next_id("project");
    if(new_id == NULL) { cJSON_Delete(projects_array); cJSON_Delete(project_json); return; }
    cJSON_AddStringToObject(project_json, "projectID", new_id);
    free(new_id);
    cJSON_AddStringToObject(project_json, "name", name);
    cJSON_AddStringToObject(project_json, "description", description);
    cJSON_AddStringToObject(project_json, "ownerID", ownerID);
    cJSON_AddStringToObject(project_json, "startDate", startDate);
    cJSON_AddStringToObject(project_json, "endDate", endDate);
    cJSON_AddStringToObject(project_json, "status", "Pending");
    cJSON *member_array = cJSON_CreateArray();
    for (int i = 0; i < currentMember; i++) {
        cJSON *member_obj = cJSON_CreateObject();
        cJSON_AddStringToObject(member_obj, "id", memberID[i]);
        cJSON_AddItemToArray(member_array, member_obj);
    }
    cJSON_AddItemToObject(project_json, "members", member_array);
    cJSON_AddItemToObject(project_json, "tasks", cJSON_CreateArray());
    cJSON_AddItemToArray(projects_array, project_json);
    write_json_to_file(JSON_PROJECT_FILE, projects_array);
    cJSON_Delete(projects_array);
}

EXPORT void delete_project_by_id(const char* projectID) {
    if (projectID == NULL) return;
    cJSON *projects_array = load_all_projects_as_json_array(JSON_PROJECT_FILE);
    if (projects_array == NULL) return;
    cJSON *new_projects_array = cJSON_CreateArray();
    if (new_projects_array == NULL) { cJSON_Delete(projects_array); return; }
    cJSON *project_item = NULL;
    cJSON_ArrayForEach(project_item, projects_array) {
        cJSON *id_json = cJSON_GetObjectItemCaseSensitive(project_item, "projectID");
        if (cJSON_IsString(id_json) && (strcmp(id_json->valuestring, projectID) != 0)) {
            cJSON_AddItemToArray(new_projects_array, cJSON_Duplicate(project_item, 1));
        }
    }
    write_json_to_file(JSON_PROJECT_FILE, new_projects_array);
    cJSON_Delete(projects_array);
    cJSON_Delete(new_projects_array);
}

EXPORT void add_task_to_project(const char* projectID, const char* title, const char* description, const char* assigneeID) {
    if (projectID == NULL || title == NULL) return;
    cJSON *projects_array = load_all_projects_as_json_array(JSON_PROJECT_FILE);
    cJSON *project_item = NULL;
    cJSON_ArrayForEach(project_item, projects_array) {
        cJSON *id_json = cJSON_GetObjectItemCaseSensitive(project_item, "projectID");
        if (cJSON_IsString(id_json) && (strcmp(id_json->valuestring, projectID) == 0)) {
            cJSON* tasks_array = cJSON_GetObjectItemCaseSensitive(project_item, "tasks");
            if (!cJSON_IsArray(tasks_array)) {
                tasks_array = cJSON_CreateArray();
                cJSON_AddItemToObject(project_item, "tasks", tasks_array);
            }
            cJSON* new_task = cJSON_CreateObject();
            char* new_task_id = get_next_id("task");
            if(new_task_id == NULL) break;
            cJSON_AddStringToObject(new_task, "taskID", new_task_id);
            free(new_task_id);
            cJSON_AddStringToObject(new_task, "title", title);
            cJSON_AddStringToObject(new_task, "description", description ? description : "");
            cJSON_AddStringToObject(new_task, "assigneeID", assigneeID ? assigneeID : "");
            cJSON_AddStringToObject(new_task, "status", "Todo");
            cJSON_AddItemToArray(tasks_array, new_task);
            break;
        }
    }
    write_json_to_file(JSON_PROJECT_FILE, projects_array);
    cJSON_Delete(projects_array);
}

EXPORT void free_c_string(char* str) {
    if (str != NULL) {
        free(str);
    }
}

EXPORT void update_task_status(const char* projectID, const char* taskID, const char* newStatus) {
    if (projectID == NULL || taskID == NULL || newStatus == NULL) return;

    cJSON *projects_array = load_all_projects_as_json_array(JSON_PROJECT_FILE);
    cJSON *project_item = NULL;

    cJSON_ArrayForEach(project_item, projects_array) {
        cJSON *p_id_json = cJSON_GetObjectItemCaseSensitive(project_item, "projectID");
        if (cJSON_IsString(p_id_json) && (strcmp(p_id_json->valuestring, projectID) == 0)) {
            
            cJSON* tasks_array = cJSON_GetObjectItemCaseSensitive(project_item, "tasks");
            if (!cJSON_IsArray(tasks_array)) {
                break;
            }

            cJSON* task_item = NULL;
            cJSON_ArrayForEach(task_item, tasks_array) {
                cJSON* t_id_json = cJSON_GetObjectItemCaseSensitive(task_item, "taskID");
                if (cJSON_IsString(t_id_json) && (strcmp(t_id_json->valuestring, taskID) == 0)) {
                    cJSON_ReplaceItemInObject(task_item, "status", cJSON_CreateString(newStatus));
                    break;
                }
            }
            break;
        }
    }

    write_json_to_file(JSON_PROJECT_FILE, projects_array);
    cJSON_Delete(projects_array);
}