# API Documentation for Simple Subscription Billing Simulator

## Overview

This document provides an overview of the API endpoints available in the Simple Subscription Billing Simulator. Each endpoint is described with its method, URL, parameters, and response format.

## Base URL

```
http://localhost:3000/api
```

## Endpoints

### 1. Create Subscription

- **Method:** POST
- **URL:** `/subscriptions`
- **Description:** Creates a new subscription for a user.
- **Request Body:**
  ```json
  {
    "userId": "string",
    "planId": "string",
    "startDate": "string (ISO 8601 date)",
    "trialPeriod": "boolean"
  }
  ```
- **Response:**
  - **201 Created**
  ```json
  {
    "subscriptionId": "string",
    "message": "Subscription created successfully."
  }
  ```

### 2. Update Subscription

- **Method:** PUT
- **URL:** `/subscriptions/:id`
- **Description:** Updates an existing subscription.
- **Parameters:**
  - `id` (path): The ID of the subscription to update.
- **Request Body:**
  ```json
  {
    "planId": "string",
    "status": "string"
  }
  ```
- **Response:**
  - **200 OK**
  ```json
  {
    "message": "Subscription updated successfully."
  }
  ```

### 3. Delete Subscription

- **Method:** DELETE
- **URL:** `/subscriptions/:id`
- **Description:** Deletes a subscription.
- **Parameters:**
  - `id` (path): The ID of the subscription to delete.
- **Response:**
  - **204 No Content**

### 4. Get Subscription Details

- **Method:** GET
- **URL:** `/subscriptions/:id`
- **Description:** Retrieves details of a specific subscription.
- **Parameters:**
  - `id` (path): The ID of the subscription.
- **Response:**
  - **200 OK**
  ```json
  {
    "subscriptionId": "string",
    "userId": "string",
    "planId": "string",
    "startDate": "string (ISO 8601 date)",
    "status": "string"
  }
  ```

### 5. List All Subscriptions

- **Method:** GET
- **URL:** `/subscriptions`
- **Description:** Retrieves a list of all subscriptions.
- **Response:**
  - **200 OK**
  ```json
  [
    {
      "subscriptionId": "string",
      "userId": "string",
      "planId": "string",
      "startDate": "string (ISO 8601 date)",
      "status": "string"
    }
  ]
  ```

## Error Handling

All error responses will follow the format:

```json
{
  "error": "string",
  "message": "string"
}
```

## Conclusion

This API documentation provides a comprehensive overview of the available endpoints for managing subscriptions in the Simple Subscription Billing Simulator. For further details on usage, please refer to the user guide and developer guide.