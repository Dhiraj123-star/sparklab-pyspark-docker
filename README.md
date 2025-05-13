# 🔥 SparkLab

A production-grade, local PySpark development environment using Docker & Docker Compose — built for data engineers and developers testing on limited local resources.

---

## 🚀 Features

- 🐳 Containerized PySpark and Flask setup (Docker & Compose)
- 💾 SQLite3 database integration for testing
- 🌐 Flask API with endpoints for CSV data, database insertion, and retrieval
- 💡 Optimized for local machines (8 GB RAM, 2 CPU cores)
- 🧼 Clean, isolated development environment
- 🔁 Auto-restart on failure
- 🔐 Production-grade structure, safe for CI/testing

---

## ⚙️ Requirements

- 🧩 Docker
- 🧩 Docker Compose

---

## ▶️ Getting Started

1. 📦 Build and run the project
2. 🌐 Access Flask API endpoints:
   - `GET /`: Health check
   - `GET /data`: Read data from CSV
   - `POST /insert`: Insert CSV data into SQLite3 database
   - `GET /db_data`: Retrieve data from SQLite3 database
3. ✅ View output logs in the container terminal
4. 🔄 Make changes to your PySpark or Flask code and rerun
5. 🧪 Test and validate locally before scaling

---

## 🛑 Stopping the App

- Gracefully shut down the environment anytime
- Cleans up volumes and orphan containers automatically

---

## 👨‍💻 Ideal For

- Data engineers building ETL prototypes
- ML engineers testing preprocessing jobs
- Backend devs integrating Spark with Flask microservices
- Students exploring distributed computing with Spark and databases

---

Crafted for efficiency. Built for growth. Welcome to **SparkLab** 🧪✨