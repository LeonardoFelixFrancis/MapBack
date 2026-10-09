# Actions API Specification

## Overview

The Actions API provides CRUD operations for named map locations.

- **Base path:** `/api/v1/actions`
- **Content type:** `application/json` for request and response bodies
- **Authentication:** No authentication is currently required by these endpoints

## Action object

```json
{
  "id": 1,
  "name": "Trailhead",
  "description": "North entrance",
  "latitude": 45.5,
  "longitude": -122.6
}
```

| Field | Type | Required on create/update | Constraints |
|---|---|---:|---|
| `id` | integer | No | Assigned by the server; returned in responses |
| `name` | string | Yes | — |
| `description` | string | Yes | — |
| `latitude` | number | Yes | Inclusive range: `-90` to `90` |
| `longitude` | number | Yes | Inclusive range: `-180` to `180` |

Both create and update require all four input fields other than `id`. Updates use `PUT` and replace the editable fields; partial updates are not supported.

## Endpoints

### Create an action

`POST /api/v1/actions/`

Request:

```json
{
  "name": "Trailhead",
  "description": "North entrance",
  "latitude": 45.5,
  "longitude": -122.6
}
```

Success: **201 Created**

```json
{
  "id": 1,
  "name": "Trailhead",
  "description": "North entrance",
  "latitude": 45.5,
  "longitude": -122.6
}
```

### List actions

`GET /api/v1/actions/`

Success: **200 OK**

Returns an array of actions, ordered by ID. An empty collection returns `[]`.

```json
[
  {
    "id": 1,
    "name": "Trailhead",
    "description": "North entrance",
    "latitude": 45.5,
    "longitude": -122.6
  }
]
```

### Get an action

`GET /api/v1/actions/{action_id}`

`action_id` is an integer.

Success: **200 OK** — returns one Action object.

If no action has that ID: **404 Not Found**

```json
{
  "detail": "Action not found"
}
```

### Replace an action

`PUT /api/v1/actions/{action_id}`

`action_id` is an integer. The request body must include all editable fields:

```json
{
  "name": "Updated trailhead",
  "description": "South entrance",
  "latitude": 40,
  "longitude": 10
}
```

Success: **200 OK** — returns the updated Action object.

If no action has that ID: **404 Not Found**

```json
{
  "detail": "Action not found"
}
```

### Delete an action

`DELETE /api/v1/actions/{action_id}`

`action_id` is an integer.

Success: **204 No Content** — response has no body.

If no action has that ID: **404 Not Found**

```json
{
  "detail": "Action not found"
}
```

## Validation errors

Requests with missing or invalid fields return **422 Unprocessable Entity** with FastAPI's standard validation-error response. For example, a latitude outside `[-90, 90]` or longitude outside `[-180, 180]` is rejected.

## Example requests

```bash
curl -X POST http://localhost:8000/api/v1/actions/ \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Trailhead\",\"description\":\"North entrance\",\"latitude\":45.5,\"longitude\":-122.6}"

curl http://localhost:8000/api/v1/actions/

curl http://localhost:8000/api/v1/actions/1

curl -X PUT http://localhost:8000/api/v1/actions/1 \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Updated trailhead\",\"description\":\"South entrance\",\"latitude\":40,\"longitude\":10}"

curl -X DELETE http://localhost:8000/api/v1/actions/1
```
