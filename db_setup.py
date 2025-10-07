# db_setup.py
import psycopg2
from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()




cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

# tables will be created here->
cur.execute("""
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department_id INT REFERENCES departments(id),
    email VARCHAR(255),
    salary DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    embedding vector(1536)  -- For OpenAI embeddings
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    employee_id INT REFERENCES employees(id),
    order_total DECIMAL(10,2),
    order_date DATE,
    embedding vector(1536)
);
""")

# will put values here->
cur.execute("""
INSERT INTO departments (name) VALUES
('HR'), ('Engineering'), ('Sales')
ON CONFLICT DO NOTHING;

INSERT INTO employees (name, department_id, email, salary) VALUES
('amaan', 1, 'amaan@gmail.com', 5000),
('purav', 2, 'purav@example.com', 7000),
('harsh', 3, 'harsh@example.com', 6000)
ON CONFLICT DO NOTHING;

INSERT INTO products (name, price) VALUES
('Laptop', 1200),
('Phone', 800),
('Monitor', 300),
('Apple', 200),
('Banana', 100),
('pen', 500),
ON CONFLICT DO NOTHING;

INSERT INTO orders (customer_name, employee_id, order_total, order_date) VALUES
('David', 1, 1500, '2025-10-01'),
('Eva', 2, 800, '2025-10-02'),
('Eva', 3, 800, '2025-11-02'),
ON CONFLICT DO NOTHING;
""")

conn.commit()
cur.close()
conn.close()
print("Database setup done!")
