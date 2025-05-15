# 🔥 SparkLab

A production-grade, local PySpark development environment using Docker & Docker Compose — built for data engineers and developers on limited local resources.

---

## 🚀 Features

- 🐳 Containerized PySpark and Flask setup (Docker & Compose)
- 💾 SQLite3 database integration
- 🌐 Flask API with endpoints for CSV data, database insertion, and retrieval
- 💡 Optimized for local machines (8 GB RAM, 2 CPU cores)
- 🧼 Clean, isolated development environment
- 🔁 Auto-restart on failure
- 🔐 Production-grade structure
- 🛠️ GitHub Actions for automated Docker image publishing

---

## ⚙️ Requirements

- 🧩 Docker
- 🧩 Docker Compose
- 🧩 GitHub account with Actions enabled
- 🧩 Docker Hub account for image publishing

---

## ▶️ Getting Started

1. 📦 Build and run the project
   ```bash
   docker-compose up --build
   ```
2. 🌐 Access Flask API endpoints:
   - `GET /`: Health check
   - `GET /data`: Read data from CSV
   - `POST /insert?mode=[overwrite|append]`: Insert CSV data into SQLite3 database
   - `GET /db_data`: Retrieve data from SQLite3 database
   - `GET /data/<name>`: Retrieve a single record by name
   - `PUT /data/<name>`: Update age for a record by name
   - `DELETE /data/<name>`: Delete a record by name
3. ✅ View output logs in the container terminal
   ```bash
   docker logs sparklab_app
   ```
4. 🔄 Make changes to your PySpark or Flask code and rerun

---

## 🛑 Stopping the App

- Gracefully shut down the environment
  ```bash
  docker-compose down
  ```
- Cleans up volumes and orphan containers automatically

---

## 🛠️ GitHub Actions Setup

1. **Add Docker Hub Secrets**:
   - In your GitHub repository, go to `Settings > Secrets and variables > Actions`.
   - Add two secrets:
     - `DOCKERHUB_USERNAME`: Your Docker Hub username (e.g., `dhiraj918106`).
     - `DOCKERHUB_TOKEN`: Your Docker Hub access token (generate at `https://hub.docker.com/settings/security`).

2. **Verify Workflow**:
   - The `.github/workflows/ci.yml` file builds and pushes the Docker image to `dhiraj918106/sparklab-pyspark-docker:latest` on `main` branch pushes.
   - Check the workflow status in the `Actions` tab of your repository.

---

## 👨‍💻 Ideal For

- Data engineers building ETL prototypes
- Backend devs integrating Spark with Flask microservices
- Students exploring distributed computing with Spark and databases

---

Crafted for efficiency. Built for growth. Welcome to **SparkLab** 🧪✨