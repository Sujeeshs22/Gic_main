Project Setup and Usage

1. Clone the Project and Create Virtual Environment

python -m venv venv

2. Activate Virtual Environment

- On Windows:
venv\\Scripts\\activate

- On macOS/Linux:
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

---

4. Run Migrations

Navigate to the root app folder gic:

cd gic

Run the migrations:

python manage.py makemigrations
python manage.py migrate

Tables will be created in the default SQLite database.

---

5. Run the Application

python manage.py runserver

---

6. CSV File Upload API

- A sample CSV folder is provided inside the upload folder.
- To upload a CSV file, send a POST request to:

{{baseurl}}/api/user/file-upload/

- In the request body, use the key file to upload the CSV file.

---

7. Expected Responses

Success Response

{
  "success": true,
  "message": {
    "saved_records": 5,
    "records_rejected": 0,
    "errors": []
  },
  "data": "File upload Successful"
}

Error Response (e.g., Duplicate Emails)

{
  "success": true,
  "message": {
    "saved_records": 0,
    "records_rejected": 5,
    "errors": [
      {
        "row": 1,
        "errors": {
          "message": "duplicate email"
        },
        "data": {
          "name": "Alice",
          "email": "alice1@example.com",
          "age": 25
        }
      }
    ]
  },
  "data": "File upload Successful"
}

The logic for CSV upload is implemented inside api_views in the common app.

---

8. Middleware Setup — API Rate Limiting

- The middleware is created inside:

common/middlewares/api_ratelimit.py

- For testing purposes and to ensure the middleware is working:
  - Change the RATE_LIMIT to 10
  - The time window is set for 5 minutes, converted to seconds and stored in the WINDOW variable.

---

9. API Rate Limiting Middleware — How It Works

The API Rate Limiting Middleware enforces a limit on the number of API requests a user or client can make within a defined time window to prevent abuse and ensure fair resource use.

- Each incoming request is tracked by storing request timestamps, typically keyed by user identity or IP address.
- The middleware checks how many requests have been made within the current time window (5 minutes).
- If the number of requests exceeds the RATE_LIMIT (e.g., 10 requests), the middleware blocks the request and returns an HTTP 429 (Too Many Requests) response.
- If the request count is within the limit, the request proceeds normally.
- This mechanism helps prevent excessive load on the server, protecting the API from spamming or misuse.

---

10. Response When Rate Limit Exceeded

If the request hits exceed the allowed number within the time window, the response will be:

{
  "error": "Too many requests"
}

Reference from - chatgpt, stackoverflow, Django documentation
