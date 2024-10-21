# RACIO Account Backend API

## Usage

1. Start the docker-compose stack

   The backend require some middleware, including PostgreSQL, Redis, and Weaviate, which can be started together using `docker-compose`.

   ```bash
   cd docker
   cp middleware.env.example middleware.env
   docker compose -f docker-compose.middleware.yaml -p dev-middleware up -d
   ```

2. Copy the environment variable configuration file:

   ```bash
   cd api
   cp .env.example .env
   ```

3. Generate a random secret key and replace the value of SECRET_KEY in the .env file:

   ```bash
   awk -v key="$(openssl rand -base64 42)" '/^SECRET_KEY=/ {sub(/=.*/, "=" key)} 1' .env > temp_env && mv temp_env .env
   ```

4. Install the required dependencies:
   RACIO Account API service uses Poetry to manage dependencies. You can execute poetry shell to activate the environment.

   ```bash
   poetry env use 3.10
   poetry install    
   ```

5. Perform the database migration:
   Before the first launch, perform database migration to the latest version:

   ```bash
   poetry shell
   flask db upgrade
   ```

6. Start backend:

   ```bash
   flask run --host 0.0.0.0 --port=5002 --debug
   ```

7. Set up your application by visiting dify apis...

   ```bash
   http://localhost:5001/console/api/setup
   {
      "step": "not_started"
   }

   http://localhost:5001/console/api/init
   {
      "status": "finished"
   }

   ```

## Testing

1. TO BE ADDED

## Build Docker Images

1.
