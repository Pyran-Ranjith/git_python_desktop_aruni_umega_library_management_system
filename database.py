# database.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        # Database configuration
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "aruni_umega_library_management"
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("✅ Connected to MySQL database")
                return True
        except Error as e:
            print(f"❌ Database connection error: {e}")
            return False
    
    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.rowcount
            
            cursor.close()
            return result
        except Error as e:
            print(f"❌ Query execution error: {e}")
            return None
    
    # Member Management
    def get_all_members(self):
        query = """
        SELECT id, member_id, name, address, phone, created_at 
        FROM members 
        ORDER BY created_at DESC
        """
        return self.execute_query(query)
    
    def add_member(self, member_id, name, address, phone):
        query = """
        INSERT INTO members (member_id, name, address, phone)
        VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (member_id, name, address, phone))
    
    def update_member(self, id, member_id, name, address, phone):
        query = """
        UPDATE members 
        SET member_id=%s, name=%s, address=%s, phone=%s
        WHERE id=%s
        """
        return self.execute_query(query, (member_id, name, address, phone, id))
    
    def delete_member(self, id):
        query = "DELETE FROM members WHERE id = %s"
        return self.execute_query(query, (id,))
    
    def get_member_by_id(self, id):
        query = "SELECT * FROM members WHERE id = %s"
        result = self.execute_query(query, (id,))
        return result[0] if result else None
    
    def get_member_by_member_id(self, member_id):
        query = "SELECT * FROM members WHERE member_id = %s"
        result = self.execute_query(query, (member_id,))
        return result[0] if result else None
    
    # Book Management
    def get_all_books(self):
        query = """
        SELECT id, book_id, title, category, author, isbn, 
               available_copies, total_copies, created_at 
        FROM books 
        ORDER BY created_at DESC
        """
        return self.execute_query(query)
    
    def get_available_books(self):
        query = """
        SELECT * FROM books 
        WHERE available_copies > 0
        ORDER BY title
        """
        return self.execute_query(query)
    
    def add_book(self, book_id, title, category, author, isbn, total_copies):
        query = """
        INSERT INTO books (book_id, title, category, author, isbn, total_copies, available_copies)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (book_id, title, category, author, isbn, total_copies, total_copies))
    
    def update_book(self, id, book_id, title, category, author, isbn, total_copies, available_copies):
        query = """
        UPDATE books 
        SET book_id=%s, title=%s, category=%s, author=%s, isbn=%s, total_copies=%s, available_copies=%s
        WHERE id=%s
        """
        return self.execute_query(query, (book_id, title, category, author, isbn, total_copies, available_copies, id))
    
    def delete_book(self, id):
        query = "DELETE FROM books WHERE id = %s"
        return self.execute_query(query, (id,))
    
    # Transactions Management
    def get_all_transactions(self):
        query = """
        SELECT t.*, m.name as member_name, b.title as book_title
        FROM transactions t
        JOIN members m ON t.member_id = m.member_id
        JOIN books b ON t.book_id = b.book_id
        ORDER BY t.issue_date DESC
        """
        return self.execute_query(query)
    
    def get_active_transactions(self):
        query = """
        SELECT t.*, m.name as member_name, b.title as book_title
        FROM transactions t
        JOIN members m ON t.member_id = m.member_id
        JOIN books b ON t.book_id = b.book_id
        WHERE t.return_date IS NULL
        ORDER BY t.issue_date DESC
        """
        return self.execute_query(query)
    
    def issue_book(self, member_id, book_id, due_date):
        query = """
        INSERT INTO transactions (member_id, book_id, issue_date, due_date, status)
        VALUES (%s, %s, %s, %s, 'issued')
        """
        issue_date = datetime.now().date()
        
        # Update book available copies
        update_book_query = "UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s AND available_copies > 0"
        
        try:
            # Start transaction
            self.connection.start_transaction()
            
            # Insert transaction
            cursor = self.connection.cursor()
            cursor.execute(query, (member_id, book_id, issue_date, due_date))
            
            # Update book copies
            cursor.execute(update_book_query, (book_id,))
            
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            self.connection.rollback()
            print(f"❌ Error issuing book: {e}")
            return False
    
    def return_book(self, transaction_id):
        query = """
        UPDATE transactions 
        SET return_date = CURDATE(), status = 'returned'
        WHERE id = %s
        """
        
        # Get book_id from transaction
        get_book_query = "SELECT book_id FROM transactions WHERE id = %s"
        
        try:
            # Start transaction
            self.connection.start_transaction()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(get_book_query, (transaction_id,))
            transaction = cursor.fetchone()
            
            if transaction:
                book_id = transaction['book_id']
                
                # Update transaction
                cursor.execute(query, (transaction_id,))
                
                # Update book available copies
                update_book_query = "UPDATE books SET available_copies = available_copies + 1 WHERE book_id = %s"
                cursor.execute(update_book_query, (book_id,))
            
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            self.connection.rollback()
            print(f"❌ Error returning book: {e}")
            return False
    
    # Statistics for Dashboard
    def get_total_members_count(self):
        query = "SELECT COUNT(*) as count FROM members"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0
    
    def get_total_books_count(self):
        query = "SELECT COUNT(*) as count FROM books"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0
    
    def get_issued_books_count(self):
        query = "SELECT COUNT(*) as count FROM transactions WHERE return_date IS NULL"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0
    
    def get_overdue_books_count(self):
        query = "SELECT COUNT(*) as count FROM transactions WHERE due_date < CURDATE() AND return_date IS NULL"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Database connection closed")