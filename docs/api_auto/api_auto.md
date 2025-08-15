# API Documentation

## `/todo/api/user/`

### POST
Create new user

**Request Body:**

{
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/UserCreate"
      }
    }
  },
  "required": true
}

**Responses:**

- 201: Successful Response
- 422: Validation Error

## `/todo/api/user/login/`

### POST
Login

**Request Body:**

{
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/UserLogin"
      }
    }
  },
  "required": true
}

**Responses:**

- 200: Successful Response
- 422: Validation Error

## `/todo/api/user/refresh/`

### POST
Refresh

**Responses:**

- 200: Successful Response

## `/todo/api/user/logout/`

### DELETE
Logout

**Responses:**

- 204: Successful Response

## `/todo/api/task/`

### POST
Create Task

**Request Body:**

{
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/TaskCreate"
      }
    }
  },
  "required": true
}

**Responses:**

- 201: Successful Response
- 422: Validation Error

## `/todo/api/task/search/`

### GET
Search Tasks

**Parameters:**

- `query` (query) - 

**Responses:**

- 200: Successful Response
- 422: Validation Error

## `/todo/api/task/all/`

### GET
Read Tasks

**Parameters:**

- `skip` (query) - 
- `limit` (query) - 

**Responses:**

- 200: Successful Response
- 422: Validation Error

## `/todo/api/task/{task_id}/`

### GET
Read Task

**Parameters:**

- `task_id` (path) - 

**Responses:**

- 200: Successful Response
- 422: Validation Error

### DELETE
Delete Task

**Parameters:**

- `task_id` (path) - 

**Responses:**

- 204: Successful Response
- 422: Validation Error

## `/todo/api/task/{task_id}/status`

### PATCH
Update Task Status

**Parameters:**

- `task_id` (path) - 

**Request Body:**

{
  "required": true,
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/TaskStatusUpdate"
      }
    }
  }
}

**Responses:**

- 200: Successful Response
- 422: Validation Error

## `/todo/api/task-collaborator/permissions/`

### POST
Assign Permissions

**Request Body:**

{
  "required": true,
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/TaskCollaboratorCreate"
      }
    }
  }
}

**Responses:**

- 200: Successful Response
- 422: Validation Error

### DELETE
Revoke Permissions

**Parameters:**

- `task_id` (query) - 
- `user_id` (query) - 

**Responses:**

- 204: Successful Response
- 422: Validation Error

## `/todo/api/task-collaborator/permissions/check_read/`

### GET
Check Read Permission

**Parameters:**

- `task_id` (query) - 

**Responses:**

- 200: Successful Response
- 422: Validation Error

## `/todo/api/task-collaborator/permissions/check_update/`

### GET
Check Update Permission

**Parameters:**

- `task_id` (query) - 

**Responses:**

- 200: Successful Response
- 422: Validation Error

