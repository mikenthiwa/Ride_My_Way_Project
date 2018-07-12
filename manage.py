import os
from werkzeug.security import generate_password_hash
import psycopg2


from app.models import create_tables


create_tables()

conn = psycopg2.connect(os.getenv('database'))
cur = conn.cursor()
hashed_password = generate_password_hash('admin2018', method='sha256')

query = "INSERT INTO users (email, username, password, is_driver, is_admin) VALUES " \
        "('admin@admin.com', 'admin', '" + hashed_password + "', '" + '1' + "','" + '1' + "' )"

cur.execute(query)
conn.commit()
conn.close()