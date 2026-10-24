
from flask import Flask, render_template, request, redirect, url_for, flash
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = "harborwing-dev-key"


@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.reservation_id,
            p.first_name,
            p.last_name,
            r.booking_date,
            r.party_size
        FROM reservation r
        JOIN passenger p
            ON r.passenger_id = p.passenger_id
        ORDER BY r.reservation_id ASC
    """)

    reservations = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("index.html", reservations=reservations)


@app.route("/add", methods=["POST"])
def add_reservation():
    passenger_id = request.form.get("passenger_id", type=int)
    party_size = request.form.get("party_size", type=int)

    if not passenger_id or not party_size or party_size < 1:
        flash("Please enter a valid passenger ID and party size.")
        return redirect(url_for("index"))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT passenger_id
            FROM passenger
            WHERE passenger_id = %s
        """, (passenger_id,))

        if cursor.fetchone() is None:
            flash("Passenger ID does not exist.")
        else:
            cursor.execute("""
                INSERT INTO reservation
                    (passenger_id, status_code, ticket_type_code,
                     travel_class_code, party_size)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                passenger_id,
                "RS01",
                "TT01",
                "TC01",
                party_size
            ))

            connection.commit()
            flash("Reservation added successfully.")

    except Exception:
        connection.rollback()
        flash("Could not add reservation. Check the database and reference codes.")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("index"))


@app.route("/update/<int:reservation_id>", methods=["POST"])
def update_reservation(reservation_id):
    party_size = request.form.get("party_size", type=int)

    if not party_size or party_size < 1:
        flash("Party size must be at least 1.")
        return redirect(url_for("index"))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE reservation
            SET party_size = %s
            WHERE reservation_id = %s
        """, (party_size, reservation_id))

        connection.commit()

        if cursor.rowcount > 0:
            flash("Reservation updated successfully.")
        else:
            flash("Reservation not found or no changes were made.")

    except Exception:
        connection.rollback()
        flash("Could not update reservation.")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:reservation_id>", methods=["POST"])
def delete_reservation(reservation_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT reservation_id
            FROM reservation
            WHERE reservation_id = %s
        """, (reservation_id,))

        if cursor.fetchone() is None:
            flash("Reservation not found.")
        else:
            cursor.execute("""
                DELETE FROM reservation_payment
                WHERE reservation_id = %s
            """, (reservation_id,))

            cursor.execute("""
                DELETE FROM reservation_leg
                WHERE reservation_id = %s
            """, (reservation_id,))

            cursor.execute("""
                DELETE FROM reservation
                WHERE reservation_id = %s
            """, (reservation_id,))

            connection.commit()
            flash("Reservation deleted successfully.")

    except Exception:
        connection.rollback()
        flash("Could not delete reservation. Check whether other records depend on it.")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("index"))


@app.route("/passengers")
def passengers():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT passenger_id, first_name, second_name,
                   last_name, email, phone
            FROM passenger
            ORDER BY passenger_id ASC
        """)
        passenger_list = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template(
        "passengers.html",
        passengers=passenger_list
    )

if __name__ == "__main__":
    app.run(debug=True)
