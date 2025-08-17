import psycopg2
import psycopg2.extras # Import the extras module
from config import load_config
from connect import connect
import time

# A simple function to encode an integer ID into a short string (Base62)
def id_to_short_url(n):
    """Encodes a positive integer into a short Base62 string."""
    if n == 0:
        return '0'
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(alphabet)
    s = ""

    while n > 0:
        s += alphabet[n % base]
        n //= base
    return s[::-1] # Reverse the string

def create_bulk_short_urls(original_urls):
    """
    Inserts a large batch of URLs, generates short URLs,
    and updates the records efficiently.
    """
    
    # SQL for bulk insert. Note the placeholder is just %s.
    # execute_values will format the data correctly.
    sql_insert = "INSERT INTO url_shortener (original_url) VALUES %s RETURNING id;"
    
    # SQL for bulk update. This is a standard pattern for bulk updates in PostgreSQL.
    sql_update = """
        UPDATE url_shortener SET short_url = data.short_url
        FROM (VALUES %s) AS data (id, short_url)
        WHERE url_shortener.id = data.id;
    """

    config = load_config()
    start_time = time.time()

    try:
        with connect(config) as conn:
            with conn.cursor() as cur:
                
                # === Step 1: Bulk INSERT and get all new IDs ===
                
                # Prepare data for insert: a list of tuples
                # The comma is important to make it a tuple: (url,)
                insert_data = [(url,) for url in original_urls]
                
                print(f"Inserting {len(insert_data)} records...")
                returned_ids = psycopg2.extras.execute_values(
                    cur,
                    sql_insert,
                    insert_data,
                    template=None,
                    fetch=True,     # Fetch the generated IDs and stores them in returned_ids
                    page_size=10000 # Adjust page_size based on memory/performance
                )
                
                # Fetch all the returned IDs
                #When fetch = true is there it returns the IDs directly
                #returned_ids = cur.fetchall()
                print(f"Successfully inserted. Received {len(returned_ids)} new IDs.")

                # === Step 2: Generate short URLs and prepare data for update ===
                
                # Create a list of tuples for the update: (id, short_url)
                update_data = []
                for row in returned_ids:
                    new_id = row[0]
                    short_url = id_to_short_url(new_id)
                    update_data.append((new_id, short_url))

                # === Step 3: Bulk UPDATE all records ===
                print(f"Updating {len(update_data)} records with short URLs...")
                psycopg2.extras.execute_values(
                    cur,
                    sql_update,
                    update_data,
                    template=None,
                    page_size=10000
                )
                print("Successfully updated records.")

            # The transaction is committed automatically when the 'with conn' block exits
            print("Transaction committed.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Database error: {error}")
        # The transaction is rolled back automatically on error
        return
        
    end_time = time.time()
    print(f"\nProcessed {len(original_urls)} records in {end_time - start_time:.2f} seconds.")


if __name__ == '__main__':
    # --- Example Usage: Generate 100,000 dummy URLs ---
    print("Generating 100,000 dummy URLs for the bulk test...")
    urls_to_add = [f"https://www.some-website.com/page/item_{i}" for i in range(100000)]
    
    # This function now handles the whole process efficiently
    create_bulk_short_urls(urls_to_add)