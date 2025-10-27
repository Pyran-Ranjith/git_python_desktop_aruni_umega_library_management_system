# test_database.py
from database import Database

def test_database():
    print("🔍 Testing database connection with actual schema...")
    
    db = Database()
    
    if db.connection and db.connection.is_connected():
        print("✅ Database connected successfully!")
        
        # Test members
        members = db.get_all_members()
        if members is not None:
            print(f"✅ Members query successful - Found {len(members)} members")
            if members:
                print("📋 Sample member:", members[0])
        
        # Test books
        books = db.get_all_books()
        if books is not None:
            print(f"✅ Books query successful - Found {len(books)} books")
        
        # Test transactions
        transactions = db.get_all_transactions()
        if transactions is not None:
            print(f"✅ Transactions query successful - Found {len(transactions)} transactions")
        
        # Test statistics
        print("\n📊 Database Statistics:")
        print(f"   Total Members: {db.get_total_members_count()}")
        print(f"   Total Books: {db.get_total_books_count()}")
        print(f"   Issued Books: {db.get_issued_books_count()}")
        print(f"   Overdue Books: {db.get_overdue_books_count()}")
        
        db.close()
    else:
        print("❌ Database connection failed!")

if __name__ == "__main__":
    test_database()