# Survey App

  This app allows users to create surveys. Other users are able to answer questions in surveys.

## Installation:
  1) clone repository
```
git clone https://github.com/backdev96/survey
```
  2) create .env file with credentials for database in /survey folder
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME={database_name} 
POSTGRES_USER={database_user}  
POSTGRES_PASSWORD={database_user_password}  
DB_HOST=database
DB_PORT=5432
```
  3) launch app
```
  docker-compose up
```
  4) App is available at 0.0.0.0:8000

## Usage:
  - documentation available at redoc/
  - testing API available at swagger/
  - default basic root at api/

#### TO DO:
    Test api with pytest
    Add statistics for surveys and questions, maybe for users
