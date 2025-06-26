# BioLab Associates - Docker Setup

This guide explains how to run the BioLab Associates application using Docker and Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start with Docker Compose

1. **Clone/Extract the project files**
2. **Navigate to the project directory**:
   ```bash
   cd _1stopshop-associates
   ```

3. **Run the application with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   - Open your browser to: `http://localhost:5000`
   - Login with: `admin` / `biolab123`

## Docker Commands

### Build and Run
```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild the image (after code changes)
docker-compose up -d --build
```

### Alternative: Direct Docker Commands
```bash
# Build the image
docker build -t biolab-associates .

# Run the container
docker run -d \
  --name biolab-associates-app \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  biolab-associates
```

## Data Persistence

The application uses Docker volumes to persist data:

- **JSON Files**: Activity logs, orders, and special orders are saved to `./data/` directory
- **Logs**: Application logs are saved to `./logs/` directory

These directories will be created automatically when you run the application.

## Configuration

### Environment Variables
You can customize the application by modifying the `docker-compose.yml` file:

```yaml
environment:
  - FLASK_ENV=development  # or production
  - FLASK_DEBUG=1          # set to 0 for production
```

### Port Mapping
To use a different port, modify the ports section in `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Access via http://localhost:8080
```

## Health Checks

The Docker container includes health checks that verify the application is running correctly:
- **Endpoint**: `http://localhost:5000/login`
- **Interval**: Every 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3 attempts

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs biolab-associates

# Check container status
docker-compose ps
```

### Port Already in Use
```bash
# Check what's using port 5000
netstat -tulpn | grep :5000

# Or modify the port in docker-compose.yml
ports:
  - "5001:5000"
```

### Data Not Persisting
Ensure the `./data` directory has proper permissions:
```bash
mkdir -p data logs
chmod 755 data logs
```

## Development Mode

For development with live code reloading, you can mount the source code:

```yaml
volumes:
  - .:/app
  - ./data:/app/data
  - ./logs:/app/logs
```

Then restart the container when you make changes:
```bash
docker-compose restart
```

## Production Deployment

For production use:

1. **Update docker-compose.yml**:
   ```yaml
   environment:
     - FLASK_ENV=production
     - FLASK_DEBUG=0
   ```

2. **Use a reverse proxy** (nginx, traefik) for SSL and load balancing

3. **Set up proper logging** and monitoring

4. **Use Docker secrets** for sensitive configuration

## Cleanup

To completely remove the application and its data:

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi biolab-associates

# Remove data (WARNING: This deletes all application data)
rm -rf data/ logs/
```

## Benefits of Docker Deployment

✅ **No Python Installation Required**: Works on any system with Docker  
✅ **Consistent Environment**: Same runtime across all machines  
✅ **Easy Deployment**: Single command to start everything  
✅ **Isolated**: Won't conflict with other applications  
✅ **Scalable**: Easy to add more services (databases, caching, etc.)  
✅ **Portable**: Works on Windows, Mac, and Linux  

## Support

If you encounter issues with the Docker setup, check:
1. Docker and Docker Compose are properly installed
2. Port 5000 is not in use by another application
3. Docker daemon is running
4. Your user has permissions to run Docker commands 