# Multi-Container Bookmark Manager (COSC349 Assignment 1)

A simple, reproducible three-tier bookmark management application built for virtualized environments using Docker and Docker Compose. 

## Architecture Overview
This system is split across three distinct containers, ensuring separation of responsibilities:
1. **Frontend (`web`):** An Nginx web server hosting a user interface built with HTML and vanilla JavaScript.
2. **Backend API (`api`):** A Python Flask application handling routing, request processing, and database communication.
3. **Storage (`db`):** A PostgreSQL database storing persistent bookmark records, preloaded with initial demonstration data upon creation.

Every user request (such as submitting a new link) flows through the full architecture: **Frontend $\rightarrow$ API $\rightarrow$ Database**.

---

## Prerequisites
* [Docker](https://www.docker.com/) and Docker Compose installed on your host system.

---

## One-Command Setup (Deployment)
To build, provision, and start the entire multi-container system with a single command, navigate to the root directory containing the `docker-compose.yml` file and run:

```bash
docker compose up --build -d
```

This automated process will:
1. Pull the necessary base images (nginx:alpine, python:3.10-slim, postgres:15-alpine).
2. Initialize the PostgreSQL database and automatically inject preloaded demonstration records via init.sql.
3. Start all three services on an isolated internal bridge network.

---

## Verification
Run the following command to verify that all three services are running:

```bash
docker compose ps
```

---

## Accessing the Application
Open your browser and navigate to http://localhost

---

## Teardown
To completely remove every resource created by the deployment, including stopped containers, networks, and the persistent database volume—run:

```bash
docker compose down -v
```