"""
MySQL Database Setup Script
Run this script to create the database and tables
"""
import pymysql
import os
from dotenv import load_dotenv
from database import Base, engine

# Load environment variables
load_dotenv()

def create_database():
    """Create the MySQL database if it doesn't exist"""
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "sdg_platform")
    
    print(f"🔗 Connecting to MySQL at {MYSQL_HOST}:{MYSQL_PORT}...")
    
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        print(f"📊 Creating database '{MYSQL_DATABASE}' if not exists...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        print(f"✅ Database '{MYSQL_DATABASE}' is ready!")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\n💡 Please check:")
        print("   1. MySQL is running")
        print("   2. Credentials in backend/.env are correct")
        print("   3. User has permission to create databases")
        return False

def create_tables():
    """Create all tables using SQLAlchemy"""
    print("\n🔨 Creating tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    print("=" * 60)
    print("   SDG DIGITAL TWIN PLATFORM - MySQL Setup")
    print("=" * 60)
    
    # Step 1: Create database
    if not create_database():
        return
    
    # Step 2: Create tables
    if not create_tables():
        return
    
    print("\n" + "=" * 60)
    print("   ✅ MySQL Setup Complete!")
    print("=" * 60)
    print("\n🚀 You can now start the backend server:")
    print("   python run_server_simple.py")
    print("\n")

if __name__ == "__main__":
    main()
