import sqlite3
import datetime

# بەستنەوەی داتابەیسی SQLite هەمیشەیی
conn = sqlite3.connect("royal_core_ultimate.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    # دروستکردنی خشتەکان بە پارێزراوی و زیادکردنی خانە نوێیەکان بەپێی ڕێنماییەکان
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS merchants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_name TEXT,
        owner_name TEXT,
        business_type TEXT,
        email TEXT UNIQUE,
        password TEXT,
        phone TEXT,
        country TEXT,
        city TEXT,
        address TEXT,
        commission_rate REAL DEFAULT 10.0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_id INTEGER,
        staff_name TEXT,
        role TEXT,
        FOREIGN KEY(merchant_id) REFERENCES merchants(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_id INTEGER,
        name TEXT,
        price REAL,
        description TEXT,
        img_url TEXT,
        FOREIGN KEY(merchant_id) REFERENCES merchants(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_id INTEGER,
        customer_name TEXT,
        customer_phone TEXT,
        staff_id INTEGER,
        booking_date TEXT,
        booking_time TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY(merchant_id) REFERENCES merchants(id),
        FOREIGN KEY(staff_id) REFERENCES staff(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        business_name TEXT,
        client_phone TEXT,
        country TEXT,
        city TEXT,
        business_type TEXT,
        address TEXT,
        ad_text TEXT,
        ad_link TEXT,
        duration_months INTEGER,
        status TEXT DEFAULT 'Pending',
        start_date TEXT,
        end_date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS page_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        view_date TEXT UNIQUE,
        view_count INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_id INTEGER,
        customer_name TEXT,
        customer_phone TEXT,
        product_details TEXT,
        total_price REAL,
        order_date TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)
    conn.commit()

    # دڵنیابوونەوە لە هەمیشەیی بوونی هەندێک خانە لە داتابەیسە کۆنەکاندا
    try:
        cursor.execute("ALTER TABLE merchants ADD COLUMN phone TEXT")
        cursor.execute("ALTER TABLE merchants ADD COLUMN country TEXT")
        cursor.execute("ALTER TABLE merchants ADD COLUMN city TEXT")
        cursor.execute("ALTER TABLE merchants ADD COLUMN address TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # خانەکان پێشتر بوونیان هەبووە

    try:
        cursor.execute("ALTER TABLE ads ADD COLUMN business_name TEXT")
        cursor.execute("ALTER TABLE ads ADD COLUMN country TEXT")
        cursor.execute("ALTER TABLE ads ADD COLUMN city TEXT")
        cursor.execute("ALTER TABLE ads ADD COLUMN business_type TEXT")
        cursor.execute("ALTER TABLE ads ADD COLUMN address TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    # ژماردنی سەردانیکەرانی ڕۆژانە بە شێوازێکی هەمیشەیی بێ تێکچوون
    today_str = datetime.date.today().isoformat()
    cursor.execute("INSERT OR IGNORE INTO page_views (view_date, view_count) VALUES (?, 0)", (today_str,))
    cursor.execute("UPDATE page_views SET view_count = view_count + 1 WHERE view_date = ?", (today_str,))
    conn.commit()

# ڕاستەوخۆ لە کاتی هاوردەکردن داتابەیسەکە ڕێکدەخات و چالاکی دەکات
init_db()
