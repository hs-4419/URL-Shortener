import time
import psycopg2
from connect import connect
from config import load_config

query = "SELECT original_url FROM url_shortener WHERE short_url IN ('abc', 'def', 'ghi', 'jkl', 'mno');"

def stress_test():
    config = load_config()
    start_time = time.time()

    try:
        with connect(config) as conn:
            with conn.cursor() as cur:
                for _ in range(1000000):
                    cur.execute(query)

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Database error: {error}")

    end_time = time.time()
    print(f"Query executed in {end_time - start_time} seconds")


if __name__ == "__main__":
    stress_test()
