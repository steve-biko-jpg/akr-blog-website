from db import get_connection

def create_admin_table():
    conn = get_connection()
    cursor = conn.cursor()

    # Create admins table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    );
    """)

    # Insert default admin user (if not exists)
    cursor.execute("""
    INSERT INTO admins (username, password)
    VALUES ('admin', SHA2('admin123', 256))
    ON DUPLICATE KEY UPDATE username=username;
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Admins table created and default admin added!")

if __name__ == "__main__":
    create_admin_table()
