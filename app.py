from datetime import date, timedelta
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "demo-secret-key"
DB_NAME = "flights.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def setup_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airline TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            travel_date TEXT NOT NULL,
            departure TEXT NOT NULL,
            arrival TEXT NOT NULL,
            duration INTEGER NOT NULL,
            price REAL NOT NULL,
            seats INTEGER NOT NULL DEFAULT 30 )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_name TEXT NOT NULL,
            email TEXT NOT NULL,
            flight_id INTEGER NOT NULL,
            booked_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (flight_id) REFERENCES flights(id) )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM flights"
    ).fetchone()[0]

    if count == 0:
        tomorrow = date.today() + timedelta(days=1)

        sample_flights = [
            ("IndiGo", "Pune", "Delhi",
             tomorrow.isoformat(), "06:30", "08:40", 130, 5200, 24),

            ("Air India", "Pune", "Delhi",
             tomorrow.isoformat(), "10:15", "12:30", 135, 6100, 18),

            ("Akasa Air", "Pune", "Delhi",
             tomorrow.isoformat(), "16:00", "18:05", 125, 4800, 12),

            ("IndiGo", "Mumbai", "Bengaluru",
             (tomorrow + timedelta(days=1)).isoformat(),
             "07:10", "08:55", 105, 4300, 20),

            ("Air India", "Delhi", "Mumbai",
             (tomorrow + timedelta(days=1)).isoformat(),
             "14:20", "16:35", 135, 5700, 16),

            ("Akasa Air", "Pune", "Goa",
             (tomorrow + timedelta(days=2)).isoformat(),
             "09:00", "10:05", 65, 3200, 14),
        ]

        conn.executemany("""
            INSERT INTO flights (
                airline, source, destination, travel_date,
                departure, arrival, duration, price, seats
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_flights)

    conn.commit()
    conn.close()

@app.route("/")
def index():
    source = request.args.get("source", "").strip()
    destination = request.args.get("destination", "").strip()
    travel_date = request.args.get("travel_date", "").strip()
    sort = request.args.get("sort", "price")

    # Only allow predefined SQL sorting options.
    sort_options = {
        "price": "price ASC",
        "departure": "departure ASC",
        "duration": "duration ASC",
    }

    order_by = sort_options.get(sort, "price ASC")

    sql = "SELECT * FROM flights WHERE seats > 0"
    params = []

    if source:
        sql += " AND source = ?"
        params.append(source)

    if destination:
        sql += " AND destination = ?"
        params.append(destination)

    if travel_date:
        sql += " AND travel_date = ?"
        params.append(travel_date)

    sql += f" ORDER BY {order_by}"

    conn = get_db()
    flights = conn.execute(sql, params).fetchall()

    sources = conn.execute(
        "SELECT DISTINCT source FROM flights ORDER BY source"
    ).fetchall()

    destinations = conn.execute(
        "SELECT DISTINCT destination FROM flights ORDER BY destination"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        flights=flights,
        sources=sources,
        destinations=destinations,
        selected_source=source,
        selected_destination=destination,
        selected_date=travel_date,
        selected_sort=sort
    )

@app.route("/book/<int:flight_id>", methods=["GET", "POST"])
def book(flight_id):
    conn = get_db()

    flight = conn.execute(
        "SELECT * FROM flights WHERE id = ?",
        (flight_id,)
    ).fetchone()

    if flight is None:
        conn.close()
        flash("Flight not found.")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("passenger_name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            flash("Please enter your name and email.")

        elif flight["seats"] < 1:
            flash("Sorry, no seats are available.")

        else:
            conn.execute("""
                INSERT INTO bookings
                (passenger_name, email, flight_id)
                VALUES (?, ?, ?)
            """, (name, email, flight_id))

            conn.execute("""
                UPDATE flights
                SET seats = seats - 1
                WHERE id = ? AND seats > 0
            """, (flight_id,))

            conn.commit()
            conn.close()

            flash("Booking saved successfully!")
            return redirect(url_for("index"))

    conn.close()
    return render_template("booking.html", flight=flight)

if __name__ == "__main__":
    setup_db()
    app.run(debug=True)
