# FinWhiz

**FinWhiz** is a finance-tracking chatbot with a microservices architecture. It includes a backend, a chatbot service, a Streamlit-based UI, and monitoring tools like Prometheus and Grafana.

## 🚀 Requirements

### System Requirements:
- **OS:** Windows, macOS, or Linux
- **RAM:** Minimum 4GB (8GB+ recommended)
- **Disk Space:** At least 10GB free (for Docker images and databases)

### Required Installations:
1. **Docker & Docker Compose**:  
   - Install Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)  
   - Install Docker Compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
   
2. **Python (optional for local development)**  
   - Install Python 3.9+: [https://www.python.org/downloads/](https://www.python.org/downloads/)

## 📄 Setup Instructions

### 1️⃣ Configure Environment Variables
Rename `sample.env` to `.env` and update values as needed:

```ini
# PostgreSQL Service
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=finance_db

# Backend Service
GROQ_API_KEY=gsk_
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres_db:5432/${POSTGRES_DB}

# Grafana Service
GF_SECURITY_ADMIN_USER=grafana
GF_SECURITY_ADMIN_PASSWORD=grafana

# Backend Query URL
BACKEND_QUERY_URL=http://backend:8000/query
```

### 2️⃣ Start the Application
Run the following command to build and start all services:

```sh
docker-compose up --build
```

### 3️⃣ Stop the Application
To stop all services, run:

```sh
docker-compose down
```

## 🛠 Clearing Docker Space

If you need to clean up unused Docker images and containers:

```sh
docker system prune -a
```

## 🌐 Accessing the Services

| Service   | URL |
|-----------|--------------------------------|
| **Backend API (Swagger UI)** | [http://localhost:8001/docs](http://localhost:8001/docs) |
| **Streamlit UI (Chatbot)** | [http://localhost:8502](http://localhost:8502) |
| **Grafana Dashboard** | [http://localhost:3001](http://localhost:3001) |
| **Prometheus Metrics** | [http://localhost:9091](http://localhost:9091) |
| **PostgreSQL** | `localhost:5433` (via pgAdmin or CLI) |

---