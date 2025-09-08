#!/bin/bash

# PyGoRP Setup Script
# This script helps you quickly set up and run the PyGoRP boilerplate

set -e

echo "🚀 Welcome to PyGoRP Setup!"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        echo "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi

    print_success "Docker and Docker Compose are installed"
}

# Check if ports are available
check_ports() {
    local ports=(3000 8080 8000 5432 6379 5050)
    local conflict=false

    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null; then
            print_warning "Port $port is already in use"
            conflict=true
        fi
    done

    if [ "$conflict" = true ]; then
        print_warning "Some ports are in use. You may need to stop other services or modify docker-compose.yml"
        echo "Press Enter to continue anyway, or Ctrl+C to abort..."
        read -r
    fi
}

# Setup environment file
setup_env() {
    if [ ! -f ".env" ]; then
        print_status "Creating .env file from template..."
        cp env.example .env
        print_success ".env file created"
    else
        print_warning ".env file already exists, skipping..."
    fi
}

# Build and start services
start_services() {
    print_status "Building and starting all services..."
    print_status "This may take a few minutes on first run..."

    docker-compose up --build -d

    print_success "Services are starting up..."
    print_status "Waiting for services to be healthy..."

    # Wait for services to be ready
    sleep 10

    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "All services are running!"
    else
        print_error "Some services failed to start. Check logs with: docker-compose logs"
        exit 1
    fi
}

# Show service status
show_status() {
    echo ""
    echo "📊 Service Status:"
    echo "=================="
    docker-compose ps

    echo ""
    echo "🌐 Access URLs:"
    echo "==============="
    echo "Frontend:        http://localhost:3000"
    echo "Backend API:     http://localhost:8080"
    echo "AI Service:      http://localhost:8000"
    echo "PgAdmin:         http://localhost:5050 (admin@pygorp.com / admin)"
    echo "PostgreSQL:      localhost:5432"
    echo "Redis:           localhost:6379"
}

# Test the setup
test_setup() {
    echo ""
    print_status "Testing services..."

    # Test backend health
    if curl -s http://localhost:8080/health > /dev/null; then
        print_success "Backend API is responding"
    else
        print_warning "Backend API is not responding yet, it may still be starting..."
    fi

    # Test AI service health
    if curl -s http://localhost:8000/health > /dev/null; then
        print_success "AI Service is responding"
    else
        print_warning "AI Service is not responding yet, it may still be starting..."
    fi

    # Test frontend
    if curl -s http://localhost:3000 > /dev/null; then
        print_success "Frontend is responding"
    else
        print_warning "Frontend is not responding yet, it may still be starting..."
    fi
}

# Main setup function
main() {
    echo ""
    print_status "Starting PyGoRP setup..."

    check_docker
    check_ports
    setup_env
    start_services
    show_status
    test_setup

    echo ""
    print_success "🎉 PyGoRP setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Open http://localhost:3000 in your browser"
    echo "2. Try creating a user through the frontend"
    echo "3. Test the AI service with some text analysis"
    echo "4. Check PgAdmin at http://localhost:5050 for database management"
    echo ""
    echo "Useful commands:"
    echo "- View logs: docker-compose logs -f"
    echo "- Stop services: docker-compose down"
    echo "- Restart services: docker-compose restart"
    echo ""
}

# Handle command line arguments
case "${1:-}" in
    "stop")
        print_status "Stopping all services..."
        docker-compose down
        print_success "Services stopped"
        ;;
    "restart")
        print_status "Restarting all services..."
        docker-compose restart
        print_success "Services restarted"
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "status")
        show_status
        ;;
    "clean")
        print_warning "This will remove all containers and volumes (including database data)!"
        echo "Are you sure? (y/N): "
        read -r confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            docker-compose down -v --remove-orphans
            print_success "All containers and volumes removed"
        fi
        ;;
    "help"|"-h"|"--help")
        echo "PyGoRP Setup Script"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  (no command)  Setup and start all services"
        echo "  stop          Stop all services"
        echo "  restart       Restart all services"
        echo "  logs          Show logs from all services"
        echo "  status        Show service status"
        echo "  clean         Remove all containers and volumes"
        echo "  help          Show this help message"
        ;;
    *)
        main
        ;;
esac
