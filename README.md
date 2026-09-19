# Customer Accounts Microservice

[![Build Status](https://github.com/fansclubcoding/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/fansclubcoding/devops-capstone-project/actions)

## Project Name
**Customer Accounts Microservice**

## Description
A RESTful microservice for managing customer accounts, built with Flask. This project demonstrates DevOps practices including CI/CD, security headers, containerization with Docker, and deployment to Kubernetes using Tekton pipelines.

## Features
- Create, Read, Update, Delete (CRUD) customer accounts
- Automated testing with nose and coverage
- Code quality checks with Flake8 and Pylint
- Security headers with Talisman
- CORS policies
- Docker containerization
- Kubernetes deployment
- CI/CD pipeline with GitHub Actions and Tekton

## Technologies
- Python 3.9
- Flask
- SQLAlchemy
- SQLite
- Docker
- Kubernetes
- GitHub Actions
- Tekton

## API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| POST | /accounts | Create a new account |
| GET | /accounts | List all accounts |
| GET | /accounts/<id> | Read an account |
| PUT | /accounts/<id> | Update an account |
| DELETE | /accounts/<id> | Delete an account |

## Author
fansclubcoding
