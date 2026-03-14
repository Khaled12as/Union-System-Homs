from supabase import create_client, Client

# استبدل هذه القيم ببيانات مشروعك من لوحة تحكم Supabase
SUPABASE_URL = "https://hrpwivxltpxqxrxyrywl.supabase.co"
SUPABASE_KEY = "sb_publishable_yWke0XGMVhH0SCuEdqnPpA_6RE2rinr"

def get_db_client() -> Client:
    """إنشاء وإرجاع كائن الاتصال بقاعدة بيانات Supabase"""
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"[خطأ في تهيئة الاتصال بقاعدة البيانات]: {e}")
        raise