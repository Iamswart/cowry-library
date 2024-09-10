# Library Management System

## Overview

This Library Management System is a distributed application consisting of two independent API services: a Frontend API for user interactions and a Backend/Admin API for administrative tasks. The system allows users to browse and borrow books, while administrators can manage the book catalog and user information.

## Table of Contents

- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.9

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>

   ```

2. Build and start the services:

   ```bash
   docker-compose up --build

   ```

## Usage

### Frontend API (http://localhost:8002)

- POST /users/enroll - Enroll a new user
- GET /books - List available books
- GET /books/<id> - Get book details
- GET /books/filter - Filter books
- POST /books/<id>/borrow - Borrow a book

### Backend/Admin API (http://localhost:8001)

- POST /admin/books - Add a new book
- DELETE /admin/books/<id> - Remove a book
- GET /admin/users - List all users
- GET /admin/users/borrowed-books - List users with borrowed books
- GET /admin/books/unavailable - List unavailable books

## Project Structure

### Database

- The system uses PostgreSQL databases for both Frontend and Backend APIs.
- Database configurations are defined in the docker-compose.yml file.

### Inter-service Communication

- Redis is used for inter-service communication.
- Changes in one service (e.g., book added in Backend API) are reflected in the other service.

### Deployment

- The project is containerized using Docker.
- Use docker-compose up --build to build and run all services.
