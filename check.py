from database import get_db_client

try:
    client = get_db_client()
    # تجربة إدراج بيانات وهمية للتحقق من الاتصال
    test_data = {
        "full_name": "Test User",
        "university_id": "0000",
        "whatsapp_number": "0000000000",
        "study_year": "السنة الأولى"
    }
    client.table("students").insert(test_data).execute()
    print("الاتصال ناجح والبيانات تم إدراجها في Supabase!")
except Exception as e:
    print(f"فشل الاتصال: {e}")