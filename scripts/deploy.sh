#!/bin/bash
set -e

# Checks if application image is specified
if [ -z "$APPLICATION_IMAGE" ]; then
  echo "[ERROR] APPLICATION_IMAGE variable not set."
  exit 1
fi

# Checks if deployment environment is specified
if [ -z "$DEPLOY_ENV" ]; then
  echo "[ERROR] DEPLOY_ENV variable not set. Please set it to 'dev' or 'prod'."
  exit 1
fi

# Defines path to deployment files
COMPOSE_PATH="/opt/rcb-deployments/discord-bot"

# Logs into GHCR using provided credentials (from GitHub CI/CD)
echo "Logging into GitHub Container Registry..."
echo "${GHCR_PAT}" | docker login ghcr.io -u "${GHCR_USER}" --password-stdin

# Pulls application image
echo "Pulling image: $APPLICATION_IMAGE"
docker pull "$APPLICATION_IMAGE"

# Prepares env and compose files based on environment
if [ "$DEPLOY_ENV" == "production" ]; then
  OVERRIDE_FILE="$COMPOSE_PATH/docker-compose.prod.yml"
  COMPOSE_FILES="-f docker-compose.yml -f docker-compose.prod.yml"
  ENV_FILE="--env-file .env.prod"
elif [ "$DEPLOY_ENV" == "development" ]; then
  OVERRIDE_FILE="$COMPOSE_PATH/docker-compose.dev.yml"
  COMPOSE_FILES="-f docker-compose.yml -f docker-compose.dev.yml"
  ENV_FILE="--env-file .env.development"
else
  echo "[ERROR] Unknown DEPLOY_ENV: $DEPLOY_ENV. Expected 'development' or 'production'."
  exit 1
fi

# Replaces placeholder string '${APPLICATION_IMAGE}' with the actual image within compose file.
echo "Injecting image into override file ($OVERRIDE_FILE)..."
sed -i "s|\${APPLICATION_IMAGE}|$APPLICATION_IMAGE|g" "$OVERRIDE_FILE"

# Changes directory to where the deployment files are
cd "$COMPOSE_PATH"

# Tears down existing containers
echo "Stopping existing containers for environment: $DEPLOY_ENV..."
docker compose -p "$PROJECT_NAME" $COMPOSE_FILES down

# Brings up new containers
echo "Starting docker-compose for environment: $DEPLOY_ENV..."
docker compose -p "$PROJECT_NAME" $ENV_FILE $COMPOSE_FILES up -d

# Cleans up unused docker images
echo "Pruning unused Docker images..."
docker image prune -f

# Announces deployment complete
echo "Deployment complete."
