import os
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


from datetime import datetime

def init_connection_pool():
    """Initialize and cache the database connection pool"""
    return ThreadedConnectionPool(
        minconn=1,
        maxconn=20,
        dsn=os.getenv('DATABASE_URL')
    )

# Get connection pool on startup
pool = init_connection_pool()

@contextmanager
def get_db_connection():
    """Get a connection from the cached pool"""
    conn = None
    try:
        conn = pool.getconn()
        conn.set_session(autocommit=True)
        yield conn
    finally:
        if conn is not None:
            pool.putconn(conn)

def save_message(session_id, role, content, msg_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chat_messages (session_id, role, content, created_at, status, msg_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (session_id, role, content, datetime.now(), "en_proceso", msg_id))
            conn.commit()

def save_waitlist_user(email, phone):
    """
    Save user to waitlist.
    Returns: str - message
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Add user
            cur.execute("""
                INSERT INTO waitlist_users (email, phone, created_at)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (email, phone, datetime.now()))
            
            return "User added to waitlist"