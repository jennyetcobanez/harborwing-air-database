"""Generate fictional HarborWing Air data. Fixed seed; refuses non-empty tables."""
import random
from datetime import date, datetime, timedelta
import mysql.connector
from faker import Faker

SEED = 20261015
random.seed(SEED)
fake = Faker()
Faker.seed(SEED)
DB_CONFIG = {"host": "localhost", "user": "root", "password": "root", "database": "harborwing_air"}  # Set password if needed.
TABLES = ["reservation_payment","reservation_leg","flight_cost","flight_leg","payment","reservation","flight_schedule","calendar_date","passenger","booking_agent","airport","airline","aircraft_type","reservation_status","ticket_type","travel_class","payment_status"]

def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        for t in TABLES:
            cur.execute(f"SELECT COUNT(*) FROM `{t}`")
            n = cur.fetchone()[0]
            if n:
                raise RuntimeError(f"Table {t} already contains {n} row(s). No data was deleted or changed.")
        airlines = [(f"AL{i:02d}", f"Demo Airline {i:02d}") for i in range(1,51)]
        cur.executemany("INSERT INTO airline (airline_code,airline_name) VALUES (%s,%s)", airlines)
        aircraft = [(f"AT{i:02d}", f"Demo Aircraft Type {i:02d}", 60+i*3) for i in range(1,51)]
        cur.executemany("INSERT INTO aircraft_type (aircraft_type_code,aircraft_type_name,seats) VALUES (%s,%s,%s)", aircraft)
        refs = [
          ("reservation_status","status_code","status_name","RS"),
          ("ticket_type","ticket_type_code","ticket_type_name","TT"),
          ("travel_class","travel_class_code","travel_class_name","TC"),
          ("payment_status","payment_status_code","payment_status_name","PS")]
        for table, cc, nc, prefix in refs:
            rows = [(f"{prefix}{i:02d}",f"Demo {table.replace('_',' ').title()} {i:02d}") for i in range(1,51)]
            cur.executemany(f"INSERT INTO `{table}` (`{cc}`,`{nc}`) VALUES (%s,%s)", rows)
        airports = [(f"A{i:02d}",f"Demonstration Airport {i+1:02d}",f"Demo City {i+1:02d}","Demo Country","Fictional training record") for i in range(50)]
        cur.executemany("INSERT INTO airport (airport_code,airport_name,city,country,other_details) VALUES (%s,%s,%s,%s,%s)", airports)
        agents = [(fake.first_name(),fake.last_name(),f"agent{i+1:03d}@example.test",fake.phone_number(),"Synthetic training record") for i in range(50)]
        cur.executemany("INSERT INTO booking_agent (first_name,last_name,email,phone,other_details) VALUES (%s,%s,%s,%s,%s)", agents)
        passengers = [(fake.first_name(),fake.last_name(),f"passenger{i+1:03d}@example.test",fake.phone_number(),fake.date_of_birth(minimum_age=18,maximum_age=85),fake.first_name() if i%3==0 else None,fake.street_address(),fake.secondary_address() if i%2==0 else None,fake.city(),fake.state(),"Fictional Country","Synthetic training record") for i in range(50)]
        cur.executemany("INSERT INTO passenger (first_name,last_name,email,phone,birth_date,second_name,address_line1,address_line2,city,state_province,country,other_details) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", passengers)
        start = date(2025,1,1)
        cal = []
        for d0 in range(730):
            d = start + timedelta(days=d0)
            cal.append((d,d.year,d.month,d.day,(d.month-1)//3+1,d.weekday()<5))
        cur.executemany("INSERT INTO calendar_date (calendar_date,year_number,month_number,day_number,quarter_number,business_day) VALUES (%s,%s,%s,%s,%s,%s)", cal)
        airport_codes = [x[0] for x in airports]
        schedules = []
        for i in range(50):
            dep = datetime(2026,1,1,6,0) + timedelta(days=i,hours=i%8)
            schedules.append((f"HW{i+1:04d}",airlines[i][0],aircraft[i][0],airport_codes[i],airport_codes[(i+1)%50],dep,dep+timedelta(hours=1+i%5)))
        cur.executemany("INSERT INTO flight_schedule (flight_number,airline_code,aircraft_type_code,origin_airport,destination_airport,scheduled_departure,scheduled_arrival) VALUES (%s,%s,%s,%s,%s,%s,%s)", schedules)
        reservations = [(i+1, i+1 if i%2 else None, f"RS{i+1:02d}", f"TT{i+1:02d}", f"TC{i+1:02d}", datetime(2026,1,1,9)+timedelta(days=i), i%5+1) for i in range(50)]
        cur.executemany("INSERT INTO reservation (passenger_id,agent_id,status_code,ticket_type_code,travel_class_code,booking_date,party_size) VALUES (%s,%s,%s,%s,%s,%s,%s)", reservations)
        payments = [(f"PS{i+1:02d}",datetime(2026,1,2,10)+timedelta(days=i),round(100+i*17.35,2),"Demo Card" if i%2==0 else "Demo Transfer",f"DEMO-PAY-{i+1:04d}") for i in range(50)]
        cur.executemany("INSERT INTO payment (payment_status_code,payment_date,amount,payment_method,reference_number) VALUES (%s,%s,%s,%s,%s)", payments)
        legs = [(x[0],x[3],x[4],x[5]+timedelta(minutes=(i%4)*5) if i%3 else None,x[6]+timedelta(minutes=(i%5)*4) if i%3 else None) for i,x in enumerate(schedules)]
        cur.executemany("INSERT INTO flight_leg (flight_number,origin_airport,destination_airport,actual_departure,actual_arrival) VALUES (%s,%s,%s,%s,%s)", legs)
        costs = [(schedules[i][0],aircraft[i][0],start+timedelta(days=i),start+timedelta(days=i+30),round(250+i*22.5,2)) for i in range(50)]
        cur.executemany("INSERT INTO flight_cost (flight_number,aircraft_type_code,valid_from,valid_to,cost) VALUES (%s,%s,%s,%s,%s)", costs)
        rp = [(i,i) for i in range(1,51)] + [(i,i+1) for i in range(1,11)]
        rl = [(i,i) for i in range(1,51)] + [(i,i+1) for i in range(1,11)]
        cur.executemany("INSERT INTO reservation_payment (reservation_id,payment_id) VALUES (%s,%s)", rp)
        cur.executemany("INSERT INTO reservation_leg (reservation_id,leg_id) VALUES (%s,%s)", rl)
        conn.commit()
        print("SUCCESS: sample data inserted. Supporting tables have 50 rows each; calendar_date has 730; link tables have 60 rows each.")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close(); conn.close()

if __name__ == "__main__":
    main()
