# test_db.py
from database import Database

def test_database():
    print("🔍 Testing database connection with actual schema...")
    
    db = Database()
    
    if db.connection and db.connection.is_connected():
        print("✅ Database connected successfully!")
        
        # Test members with actual schema
        members = db.get_all_members()
        if members is not None:
            print(f"✅ Members query successful - Found {len(members)} members")
            if members:
                print("📋 Member columns available:", list(members[0].keys()))
                print("👤 First member sample:")
                member = members[0]
                print(f"   ID: {member['id']}")
                print(f"   Member ID: {member['member_id']}")
                print(f"   Name: {member['name']}")
                print(f"   Phone: {member['phone']}")
        else:
            print("❌ Members query failed")
        
        # Test adding a new member
        print("\n🧪 Testing member creation...")
        result = db.add_member("MEM2024001", "John Doe", "123 Main Street", "123-456-7890")
        if result:
            print("✅ Member added successfully!")
        else:
            print("⚠️ Could not add test member (might already exist)")
        
        # Test statistics
        print("\n📊 Database Statistics:")
        print(f"   Total Members: {db.get_total_members_count()}")
        print(f"   Total Books: {db.get_total_books_count()}")
        print(f"   Borrowed Books: {db.get_borrowed_books_count()}")
        print(f"   Overdue Books: {db.get_overdue_books_count()}")
        
        db.close()
    else:
        print("❌ Database connection failed!")
        print("💡 Please check:")
        print("   - Is MySQL server running?")
        print("   - Are the database credentials correct?")
        print("   - Does the database 'library_management_system' exist?")
        print("   - Does the 'members' table exist with the correct schema?")

if __name__ == "__main__":
    test_database()