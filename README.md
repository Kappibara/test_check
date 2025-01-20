# How to Run the App with Docker-Compose

## Prerequisites

Before starting, ensure that you have **Docker Compose** installed. If you don't have it, follow the [official installation guide](https://docs.docker.com/compose/install/).

---

## Step 1: Set Up the Environment File

1. Navigate to the `src` directory and create a `.env` file from the provided `.env.template`:
   ```bash
   pwd
   cd src/
   cp .env.template .env
   cd ..
   ```
2. Open the `.env` file and populate it with the required environment variables. Below is an example configuration:

```aiignore
SECRET_KEY="mysecret"                    # Secret key for encryption
ALGORITHM="HS256"                        # Algorithm for JWT signing
ACCESS_TOKEN_EXPIRE_MINUTES=30           # Token expiration time in minutes
DB_USER="postgres"                       # Database username
DB_PASS="postgres"                       # Database password
DB_HOST="database"                       # Database host in docker container
DB_PORT=5432                             # Database port
DB_NAME="postgres"                       # Database name
```

---

## Step 2: Build and Run the Application

Once the `.env` file is ready, use the following commands to build and run the application:


### Build the Docker Images
```
docker-compose build
```
or
```
docker compose build
```

### Start the Application
```
docker-compose up
```
or 
```
docker compose up
```
Open your browser and navigate to [https://localhost/docs#](https://localhost/docs#) or [https://127.0.0.1/docs#](https://127.0.0.1/docs#) to check your local server's status.


### Stop and Remove Containers
```
docker-compose down
```
or 
```
docker compose down
```

