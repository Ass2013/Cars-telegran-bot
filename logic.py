import sqlite3
from config import DATABASE


class DatabaseManager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)

        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")

        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS brands (
                    brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand_name TEXT NOT NULL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS engine (
                    engine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    engine_name TEXT NOT NULL,
                    engine_cylinders TEXT,
                    engine_fuel_type TEXT,
                    brand_id INTEGER,
                    FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT UNIQUE,
                    brand_id INTEGER,
                    engine_id INTEGER,
                    FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
                    FOREIGN KEY (engine_id) REFERENCES engine(engine_id)
                )
            """)

        conn.close()

    def seed_data(self):
        conn = sqlite3.connect(self.database)

        with conn:
            # Brands
            brands = [
                ('Toyota',), ('Volkswagen',), ('Ford',), ('BMW',),
                ('Mercedes-Benz',), ('Audi',), ('Honda',), ('Hyundai',),
                ('Nissan',), ('Kia',), ('Chevrolet',), ('Peugeot',),
                ('Renault',), ('Skoda',), ('Fiat',), ('Volvo',),
                ('Mazda',), ('Subaru',), ('Jeep',), ('Land Rover',),
                ('Porsche',), ('Ferrari',), ('Lamborghini',), ('Maserati',),
                ('Bentley',), ('Rolls-Royce',), ('Tesla',), ('Jaguar',),
                ('Mini',), ('Alfa Romeo',)
            ]
            conn.executemany(
                "INSERT OR IGNORE INTO brands (brand_name) VALUES (?)",
                brands
            )

            # Engines
            engines = [
                ('Inline-3', '3', 'Petrol', None),
                ('Inline-4', '4', 'Petrol', None),
                ('Inline-4 Turbo', '4', 'Petrol', None),
                ('Inline-4 Diesel', '4', 'Diesel', None),
                ('Inline-5', '5', 'Petrol', None),
                ('V6', '6', 'Petrol', None),
                ('V6 Diesel', '6', 'Diesel', None),
                ('V8', '8', 'Petrol', None),
                ('V8 Twin Turbo', '8', 'Petrol', None),
                ('V10', '10', 'Petrol', None),
                ('V12', '12', 'Petrol', None),
                ('Boxer 4', '4', 'Petrol', None),
                ('Boxer 6', '6', 'Petrol', None),
                ('Electric Single Motor', '0', 'Electric', None),
                ('Electric Dual Motor', '0', 'Electric', None),
                ('Hybrid Inline-4', '4', 'Hybrid', None),
                ('Plug-in Hybrid', '4', 'Hybrid', None)
            ]
            conn.executemany(
                """INSERT OR IGNORE INTO engine
                (engine_name, engine_cylinders, engine_fuel_type, brand_id)
                VALUES (?, ?, ?, ?)""",
                engines
            )

        conn.close()

    # Corrected add_user method
    def add_user(self, user_name):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute(
                "INSERT OR IGNORE INTO users (user_name) VALUES (?)",
                (user_name,)
            )
        conn.close()

    def get_users(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
        conn.close()
        return users


if __name__ == "__main__":
    db = DatabaseManager(DATABASE)
    db.create_tables()
    db.seed_data()
    print("Database, tables, and seed data created successfully.")