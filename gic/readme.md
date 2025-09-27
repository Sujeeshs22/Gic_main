Project Setup and Usage

1. Clone the Project and Create Virtual Environment

python -m venv venv

2. Activate Virtual Environment

- On Windows:
venv\\Scripts\\activate

- On macOS/Linux:
source venv/bin/activate

3. Install Dependencies
In cmd run-
 pip install -r requirements.txt

---

4. Run Migrations

Navigate to the root app folder gic:

cd gic

Run the migrations:

python manage.py makemigrations
python manage.py migrate

[!IMPORTANT]:
If you encounter issues detecting models, run:
run - "python manage.py makemigrations common"
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

