import streamlit as st
import psycopg2
import numpy as np
import ast
from config import DB_CONFIG
from config import OPENAI_API_KEY

st.title("Natural Language Search Demo (Test Mode)")

# DB
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()


import openai

openai.api_key = OPENAI_API_KEY

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002" 
    )
    return np.array(response['data'][0]['embedding'], dtype=float)







def vector_search(table, query, top_k=3):
    query_emb = get_embedding(query).astype(float)
    
    if table == "orders":
        cur.execute(f"SELECT id, customer_name, embedding FROM {table}")
    else:
        cur.execute(f"SELECT id, name, embedding FROM {table}")
    
    results = []
    for row in cur.fetchall():
        # string to list 
        vec = np.array(ast.literal_eval(row[2]), dtype=float)
        # cosine similarity
        sim = np.dot(query_emb, vec) / (np.linalg.norm(query_emb) * np.linalg.norm(vec))
        results.append((row[0], row[1], sim))
    results.sort(key=lambda x: x[2], reverse=True)
    return results[:top_k] 



query = st.text_input("Ask something about employees, orders, or products:")

if st.button("Search"):
    st.write("Searching...")
    
    st.subheader("Products")
    products = vector_search("products", query)
    for pid, name, sim in products:
        st.write(f"{name} (similarity: {sim:.2f})")

    st.subheader("Orders")
    orders = vector_search("orders", query)
    for oid, name, sim in orders:
        st.write(f"{name} (similarity: {sim:.2f})")
