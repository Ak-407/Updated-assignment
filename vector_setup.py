import psycopg2
import numpy as np
from config import DB_CONFIG, OPENAI_API_KEY

import openai

# Set OpenAI API key in config file
openai.api_key = OPENAI_API_KEY

# Function to get embedding from OpenAI
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"  # recommended embedding model
    )
    return np.array(response['data'][0]['embedding'], dtype=float)



# will conect the detabase-> DB
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# it will get given data in paramerters from database 
cur.execute("SELECT id, name FROM products")
for pid, name in cur.fetchall():
    # it will convert into numpy array which cannot be directly stored in database
    emb = get_embedding(name)
    # so will use this to converrt numpy array into a list
    emb_list = [float(x) for x in emb]  # float list
    cur.execute(
        "UPDATE products SET embedding = %s WHERE id = %s",
        (emb_list, pid)
    )


# similarly for orders
cur.execute("SELECT id, customer_name FROM orders")
for oid, cname in cur.fetchall():
    emb = get_embedding(cname)
    emb_list = [float(x) for x in emb]
    cur.execute(
        "UPDATE orders SET embedding = %s WHERE id = %s",
        (emb_list, oid)
    )

conn.commit()
cur.close()
conn.close()
print("Vector embeddings populated successfully!")


