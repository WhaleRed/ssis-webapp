from supabase import create_client
from config import DB_URL, DB_KEY

supabase = create_client(DB_URL, DB_KEY)

def get_db():
    return supabase