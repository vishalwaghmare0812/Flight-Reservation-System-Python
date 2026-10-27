# Flight Booking System

A web-based flight booking application developed using **Python, Flask, and SQLite**. Search flights, compare fares, check seat availability, and book flights through a simple and user-friendly interface.

## Features

- **Flight Search:** Search flights by source, destination, and travel date.
- **Fare Comparison:** Sort flights by price, departure time, or duration.
- **Seat Availability:** View available seats before booking.
- **Flight Booking:** Book flights using passenger name and email.
- **Database Management:** Store flight details and booking records using SQLite.
- **Sample Data:** Automatically populate sample flights on the first run.

## Technology Stack

- Python
- Flask
- SQLite
- HTML/CSS

## Installation and Setup

- Python 3.9 or later
- pip

### 1. Clone the Repository

    git clone https://github.com/vishalwaghmare0812/Flight-Reservation-System-Python.git
    cd Flight-Reservation-System-Python

### 2. Install Dependencies

    pip install Flask

### 3. Run the Application

    python app.py

### 4. Access the Application

Open your browser and visit:

http://127.0.0.1:5000

The SQLite database (`flights.db`) and sample flight records are initialized automatically when the application starts.

## Project Structure

    flight-booking-system/
    ├── app.py
    ├── flights.db
    └── templates/
        ├── index.html
        └── booking.html

**Built with Python, Flask, and SQLite.**
