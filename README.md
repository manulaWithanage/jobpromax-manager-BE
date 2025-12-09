# JobProMax Progress Hub - Backend

This is the backend API for the JobProMax Progress Hub, built with Python (FastAPI) and MongoDB (Beanie).

## Tech Stack
- **Framework**: FastAPI
- **Database**: MongoDB (Async using Motor & Beanie)
- **Environment Management**: Pydantic Settings

## Prerequisites
- Python 3.8+
- MongoDB installed and running locally on port 27017

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/manulaWithanage/jobpromax-manager-BE.git
    cd jobpromax-manager-BE
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:
    - **Windows**:
        ```bash
        venv\Scripts\activate
        ```
    - **Mac/Linux**:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Environment Configuration**:
    - Ensure you have a `.env` file in the root directory.
    - Example content:
        ```env
        MONGODB_URI=mongodb://localhost:27017
        DATABASE_NAME=progress_hub
        ALLOWED_ORIGINS=["http://localhost:3000"]
        ```

## Database Seeding
To populate the database with initial mock data:
```bash
python seed.py
```

## Running the Server
Start the development server with live reload:
```bash
uvicorn app.main:app --reload
```
The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Documentation
Interactive API docs (Swagger UI) are available at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure
```
.
├── app/
│   ├── models/       # Beanie/Pydantic data models
│   ├── routes/       # API endpoints
│   ├── config.py     # Environment configuration
│   ├── database.py   # Database connection logic
│   └── main.py       # Application entry point
├── requirements.txt  # Project dependencies
├── seed.py           # Database seeding script
└── .env              # Environment variables
```
