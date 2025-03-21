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
  - [Create Deal](#create-deal)
  - [Create Ticket](#create-ticket)
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
1. ### Register
    URL: `/api/register`
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
        "phone": "08123456789"
    }
    ```

    Response Body

    ```json
    {
        "data": {
            "contact": {
                "createdate": "2025-03-21T15:53:16.679Z",
                "email": "koikibabatun@gmail.com",
                "firstname": "Baba",
                "hs_all_contact_vids": "107824580901",
                "hs_associated_target_accounts": "0",
                "hs_currently_enrolled_in_prospecting_agent": "false",
                "hs_email_domain": "gmail.com",
                "hs_full_name_or_email": "Baba Tunde",
                "hs_is_contact": "true",
                "hs_is_unworked": "true",
                "hs_lifecyclestage_lead_date": "2025-03-21T15:53:16.679Z",
                "hs_marketable_status": "false",
                "hs_marketable_until_renewal": "false",
                "hs_membership_has_accessed_private_content": "0",
                "hs_object_id": "107824580901",
                "hs_object_source": "INTEGRATION",
                "hs_object_source_id": "9231478",
                "hs_object_source_label": "INTEGRATION",
                "hs_pipeline": "contacts-lifecycle-pipeline",
                "hs_prospecting_agent_actively_enrolled_count": "0",
                "hs_registered_member": "0",
                "hs_searchable_calculated_phone_number": "8180854296",
                "hs_sequences_actively_enrolled_count": "0",
                "id": "107824580901",
                "lastmodifieddate": "2025-03-21T15:53:16.679Z",
                "lastname": "Tunde",
                "lifecyclestage": "lead",
                "num_notes": "0",
                "phone": "08180854296"
            }
        },
        "message": "User registered successfully"
    }
    ```

    #### Account already exists
    ```json
    {
        "error": "User already exists"
    }
    ```

2. ### Login
    URL: `/api/login`
    Method: POST
    Authorization: False
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

3. ### Get Contacts
    URL: `/api/new-crm-objects?limit<int|nullable>&cursor<string|nullable>`
    Method: GET
    Authorization: True
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

4. ### Create Deal
    URL: `/api/deals`
    Method: POST
    Authorization: True
    Description: Creates a new deal for the authenticated user's contact info
    Request Body:
    The dealstage can be one of `appointmentscheduled`, `qualifiedtobuy`, `presentationscheduled`, `decisionmakerboughtin`, `contractsent`, `closedwon`, `closedlost`
    ```json
        {
            "dealname": "Test Deal",
            "dealstage": "appointmentscheduled",
            "amount": 1000000,
            "description": "This is a test deal"
        }
    ```

    Response Body:
    ```json
    {
        "data": {
            "amount": "1000000.0",
            "amount_in_home_currency": "1000000.0",
            "createdate": "2025-03-21T15:06:02.943Z",
            "days_to_close": "0",
            "dealname": "Another Deal",
            "dealstage": "appointmentscheduled",
            "description": "This is a test deal",
            "hs_closed_amount": "0",
            "hs_closed_amount_in_home_currency": "0",
            "hs_closed_deal_close_date": "0",
            "hs_closed_deal_create_date": "0",
            "hs_closed_won_count": "0",
            "hs_days_to_close_raw": "0",
            "hs_deal_stage_probability": "0.200000000000000011102230246251565404236316680908203125",
            "hs_deal_stage_probability_shadow": "0.200000000000000011102230246251565404236316680908203125",
            "hs_forecast_amount": "1000000.0",
            "hs_is_closed": "false",
            "hs_is_closed_count": "0",
            "hs_is_closed_won": "false",
            "hs_is_open_count": "1",
            "hs_lastmodifieddate": "2025-03-21T15:06:19.980Z",
            "hs_object_id": "34915256103",
            "hs_object_source": "INTEGRATION",
            "hs_object_source_id": "9231478",
            "hs_object_source_label": "INTEGRATION",
            "hs_open_deal_create_date": "1742569562943",
            "hs_projected_amount": "200000.0000000000111022302462515654042363166809082031250000000",
            "hs_projected_amount_in_home_currency": "200000.0000000000111022302462515654042363166809082031250000000",
            "hs_v2_date_entered_current_stage": "2025-03-21T15:06:02.943Z",
            "hs_v2_time_in_current_stage": "2025-03-21T15:06:02.943Z",
            "id": "34915256103",
            "pipeline": "default"
        },
        "message": "Deal created successfully"
    }
    ```

5. ### Create Ticket
    URL: `api/tickets/<deal_id>`
    Method: POST
    Authorization: True
    Desription:
    Request Body:
    The category can be one of `general_inquiry`, `technical_issue`, `billing`, `service_request`, `meeting`.
    ```json
    {
        "subject": "Test Ticket",
        "description": "This is a test ticket",
        "category": "general_inquiry",
        "pipeline": "0",
        "hs_ticket_priority": "HIGH",
        "hs_pipeline_stage": "1"
    }
    ```

    Response Body:
    ```json
    {
        "data": {
            "category": "general_inquiry",
            "closed_date": "2025-03-21T15:35:54.252Z",
            "createdate": "2025-03-21T15:35:54.252Z",
            "description": "This is a test ticket",
            "hs_helpdesk_sort_timestamp": "2025-03-21T15:35:54.252Z",
            "hs_is_visible_in_help_desk": "true",
            "hs_last_message_from_visitor": "false",
            "hs_lastmodifieddate": "2025-03-21T15:35:54.252Z",
            "hs_num_associated_companies": "0",
            "hs_num_associated_conversations": "0",
            "hs_num_times_contacted": "0",
            "hs_object_id": "21675753358",
            "hs_object_source": "INTEGRATION",
            "hs_object_source_id": "9231478",
            "hs_object_source_label": "INTEGRATION",
            "hs_pipeline": "0",
            "hs_pipeline_stage": "4",
            "hs_ticket_id": "21675753358",
            "hs_ticket_priority": "LOW",
            "id": "21675753358",
            "num_notes": "0",
            "pipeline": "test",
            "subject": "Test Ticket",
            "time_to_close": "0"
        },
        "message": "Ticket created successfully"
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
