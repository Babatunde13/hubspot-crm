# Hubspot CRM API

This is an API built with Flask, PostgreSQL, and Hubspot API integration. The API allows users to create contacts, deals and tickets. It also allows authenticated users to search created contacts, deals, tickets.

## Table of Contents

- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running The API](#running-the-api)
- [Endpoints](#endpoints)
  - [Get Pipelines and Their stages](#get-pipelines-and-their-stages)
  - [Register](#register)
  - [Login](#login)
  - [Search Contacts](#get-contacts)
- [Error Codes](#error-codes)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Babatunde13/hubspot-crm.git
   cd hubspot-crm
   ```
2. Build the Docker containers:
    ```
    docker-compose up --build
    ```
3. The API will be running at http://localhost:4012 once the containers are started.

## Environment Variables
```bash
SECRET_KEY=
DATABASE_URL=
SQLALCHEMY_TRACK_MODIFICATIONS=
JWT_SECRET_KEY=
PORT=
OPENAI_API_KEY=
FLASK_ENV=
HUBSPOT_CLIENT_ID=
HUBSPOT_CLIENT_SECRET=
HUBSPOT_REFRESH_TOKEN=
```

### Running The API
To run the Api, you can run it with `python run.py` if you already have your database setup and set in the environment variable (`DATABASE_URL`). Alternatively, you can run the API with the command below, this persists the DB so if you restart the container you still have access to your existing data
```bash
docker-compose up
```

## Endpoints
1. ### Get Pipelines and Their stages
    URL: `/contacts/pipelines`
    Method: GET
    Authorization: False
    Description: Retrieves all the pipelines and list of stages per pipeline. This helps us to know which value can be set for `pipeline` and `hs_pipeline_stage` during User creation. We choose an id and set it to the value of `pipeline`, we then choose one of the available stages for the chosen pipeline and set it to `hs_pipeline_stage`

    Response body
    ```json
        {
            "data": {
                "data": [
                {
                    "id": "0",
                    "label": "Support Pipeline",
                    "stages": [
                    {
                        "display_order": 0,
                        "id": "1",
                        "label": "New"
                    },
                    {
                        "display_order": 1,
                        "id": "2",
                        "label": "Waiting on contact"
                    },
                    {
                        "display_order": 2,
                        "id": "3",
                        "label": "Waiting on us"
                    },
                    {
                        "display_order": 3,
                        "id": "4",
                        "label": "Closed"
                    }
                    ]
                }
                ]
            },
            "message": "Pipeline tickets retrieve successfully"
        }
    ```


2. ### Register
    URL: `/register`
    Method: POST
    Authorization: False
    Description: Creates a new user and saves/update their info on hubspot.
    Request Body:
    To get the valid `pipeline` and `hs_pipeline_stage`

    ```json
    {
        "email": "koikibabatunde15@gmail.com",
        "firstname": "Babatunde",
        "lastname": "Koiki",
        "password": "passworD@#1",
        "phone": "08123456789",
        "deals": [
            {
                "dealname": "Test Deal",
                "dealstage": "appointmentscheduled",
                "amount": 1000000,
                "description": "This is a test deal",
                "tickets": [
                    {
                        "subject": "Test Ticket",
                        "description": "This is a test ticket",
                        "category": "PRODUCT_ISSUE",
                        "pipeline": "0",
                        "hs_ticket_priority": "HIGH",
                        "hs_pipeline_stage": "1"
                    }
                ]
            }
        ]
    }
    ```

    Response Body

    ```json
    {
        "message": "User registered successfully",
        "data": {}
    }
    ```

    #### Account already exists
    ```json
    {
        "error": "User already exists"
    }
    ```

3. ### Login
    URL: `/login`
    Method: POST
    Description: Login a user
    Request Body:

    ```json
    {
        "email": "string",
        "password": "string|required|min=6",
    }
    ```

    Response Body

    ```json
    {
        "message": "User authenticated successfully",
        "data": {
            "access_token": "<token>"
        }
    }
    ```

    #### Account does not exist/invalid password
    ```json
    {
        "error": "Invalid credentials"
    }
    ```

4. ### Get Contacts
    URL: `/contacts?limit<int|nullable>&cursor<string|nullable>`
    Method: GET
    Description: Gets paginated list of contacts with their associated 
    Request Query:
        1. limit: Maximum number of contacts that should be returned, defaults to 10.
        2. cursor: The start cursor. Returned contacts starts after this value, if not passed it starts fetching from the beginning.

    Response Body

    ```json
    {
        "data": {
            "data": {
            "contacts": [
                {
                    "createdate": "2025-03-20T19:08:14.591Z",
                    "deals": [],
                    "email": "koikibabatunde15@gmail.com",
                    "firstname": "Babatunde",
                    "hs_object_id": "107583182849",
                    "id": "107583182849",
                    "lastmodifieddate": "2025-03-20T19:13:17.740Z",
                    "lastname": "Koiki"
                },
                {
                    "createdate": "2025-03-20T16:15:20.045Z",
                    "deals": [
                        {
                            "amount": "1000000",
                            "closedate": null,
                            "createdate": "2025-03-20T16:56:49.494Z",
                            "dealname": "Test Deal",
                            "dealstage": "appointmentscheduled",
                            "hs_lastmodifieddate": "2025-03-20T17:57:50.720Z",
                            "hs_object_id": "34888041733",
                            "id": "34888041733",
                            "pipeline": "default",
                            "tickets": [
                                {
                                    "category": "PRODUCT_ISSUE",
                                    "createdate": "2025-03-20T17:49:20.891Z",
                                    "description": "This is a test ticket",
                                    "hs_lastmodifieddate": "2025-03-20T17:49:24.554Z",
                                    "hs_object_id": "21629940647",
                                    "hs_pipeline_stage": "1",
                                    "hs_ticket_priority": "HIGH",
                                    "id": "21629940647",
                                    "pipeline": "0",
                                    "subject": "Test Ticket"
                                },
                                {
                                    "category": "PRODUCT_ISSUE",
                                    "createdate": "2025-03-20T19:00:36.745Z",
                                    "description": "This is a test ticket",
                                    "hs_lastmodifieddate": "2025-03-20T19:01:05.284Z",
                                    "hs_object_id": "21656429426",
                                    "hs_pipeline_stage": "1",
                                    "hs_ticket_priority": "HIGH",
                                    "id": "21656429426",
                                    "pipeline": "0",
                                    "subject": "Test Ticket"
                                },
                                {
                                    "category": "PRODUCT_ISSUE",
                                    "createdate": "2025-03-20T19:00:53.548Z",
                                    "description": "This is a test ticket",
                                    "hs_lastmodifieddate": "2025-03-20T19:01:35.207Z",
                                    "hs_object_id": "21659687261",
                                    "hs_pipeline_stage": "1",
                                    "hs_ticket_priority": "HIGH",
                                    "id": "21659687261",
                                    "pipeline": "0",
                                    "subject": "Test Ticket"
                                },
                                {
                                    "category": "PRODUCT_ISSUE",
                                    "createdate": "2025-03-20T19:08:17.190Z",
                                    "description": "This is a test ticket",
                                    "hs_lastmodifieddate": "2025-03-20T19:08:20.662Z",
                                    "hs_object_id": "21665209971",
                                    "hs_pipeline_stage": "1",
                                    "hs_ticket_priority": "HIGH",
                                    "id": "21665209971",
                                    "pipeline": "0",
                                    "subject": "Test Ticket"
                                }
                            ]
                        }
                    ],
                    "email": "koikibabatunde14@gmail.com",
                    "firstname": "Babatunde",
                    "hs_object_id": "107599160232",
                    "id": "107599160232",
                    "lastmodifieddate": "2025-03-20T16:57:02.792Z",
                    "lastname": "Koiki"
                }
            ],
            "next_after": "107599160233"
            }
        },
        "message": "Contacts retrieved successfully"
    }
    ```

## Error Codes
The API will return the following common error codes and messages:

Status Code	Error Message	Description
400	Validation error	Input validation failed, such as missing or invalid fields.
401	Invalid token	Authentication failed. Invalid or expired 
JWT token.
429	ratelimit exceeded 1 per 1 minute. Rate limit expired.
404	Resource not found	The requested resource is not found.
500	Internal server error	Something went wrong on the server side.
