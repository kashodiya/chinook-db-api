# Chinook Digital Media Store API

A comprehensive RESTful API for the Chinook digital media store database built with FastAPI and SQLAlchemy.

## Overview

This project provides a complete API for managing a digital media store, including endpoints for artists, albums, tracks, customers, employees, invoices, playlists, genres, and media types. The API is built on top of the Chinook SQLite database, which represents a digital media store with tables for artists, albums, media tracks, invoices, and customers.

## Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete operations for all entities
- **Relationship Management**: Handle relationships between entities (e.g., artists and albums, playlists and tracks)
- **Search Functionality**: Search for tracks, customers, and other entities
- **Interactive API Documentation**: Auto-generated Swagger UI documentation

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library
- **Pydantic**: Data validation and settings management
- **SQLite**: Lightweight disk-based database (Chinook database)
- **Uvicorn**: ASGI server for running the FastAPI application

## API Endpoints

The API provides the following main endpoints:

- `/artists`: Manage artists
- `/albums`: Manage albums
- `/tracks`: Manage tracks
- `/customers`: Manage customers
- `/employees`: Manage employees
- `/invoices`: Manage invoices and invoice lines
- `/playlists`: Manage playlists and playlist tracks
- `/genres`: Manage genres
- `/media-types`: Manage media types

Each endpoint supports standard HTTP methods (GET, POST, PUT, DELETE) for CRUD operations.

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kashodiya/chinook-db-api.git
   cd chinook-db-api
   ```

2. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic
   ```

3. Run the application:
   ```bash
   python run.py
   ```

4. Access the API documentation:
   Open your browser and navigate to `http://localhost:56313/docs`

## Database Schema

The Chinook database includes the following main tables:

- **Artist**: Music artists
- **Album**: Music albums
- **Track**: Individual music tracks
- **Genre**: Music genres
- **MediaType**: Types of media (e.g., MPEG audio, AAC audio)
- **Playlist**: Collections of tracks
- **Customer**: Store customers
- **Employee**: Store employees
- **Invoice**: Customer invoices
- **InvoiceLine**: Individual line items on invoices

## API Documentation

The API documentation is automatically generated and available at `/docs` when the server is running. It provides a complete reference of all endpoints, request/response models, and allows for interactive testing of the API.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Chinook database is a sample database available for SQL Server, Oracle, MySQL, etc. It can be created by running a single SQL script.
- This project was inspired by the need for a comprehensive API for the Chinook database.
