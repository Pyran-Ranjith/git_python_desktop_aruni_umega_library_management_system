# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database import Database
from styles import Styles

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.setup_ui()
        
        # Load initial data
        self.load_members()
        self.load_books()
        self.load_transactions()
    
    def setup_ui(self):
        # Main window configuration
        self.root.title("Aruni Umega Library Management System")
        self.root.geometry("1300x750")
        self.root.configure(bg=Styles.LIGHT)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_members_tab()
        self.create_books_tab()
        self.create_transactions_tab()
    
    def create_dashboard_tab(self):
        # Dashboard Tab
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Header
        header_label = tk.Label(dashboard_frame, 
                               text="🏛️ Aruni Umega Library Management System", 
                               font=Styles.HEADING_FONT,
                               bg=Styles.PRIMARY,
                               fg="white",
                               pady=20)
        header_label.pack(fill=tk.X, padx=10, pady=10)
        
        # Stats Frame
        stats_frame = tk.Frame(dashboard_frame, bg=Styles.LIGHT)
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Stats cards
        stats_data = [
            ("📚 Total Books", self.db.get_total_books_count(), Styles.INFO),
            ("👥 Total Members", self.db.get_total_members_count(), Styles.SUCCESS),
            ("📖 Books Issued", self.db.get_issued_books_count(), Styles.WARNING),
            ("⏰ Overdue Books", self.db.get_overdue_books_count(), Styles.DANGER)
        ]
        
        for i, (title, value, color) in enumerate(stats_data):
            card = Styles.create_card(stats_frame)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            card.config(pady=20)
            
            tk.Label(card, text=title, font=Styles.NORMAL_FONT, bg=Styles.WHITE).pack(pady=(10, 5))
            tk.Label(card, text=str(value), font=Styles.HEADING_FONT, bg=Styles.WHITE, fg=color).pack(pady=(0, 10))
            
            stats_frame.columnconfigure(i, weight=1)
    
    def create_members_tab(self):
        # Members Tab
        members_frame = ttk.Frame(self.notebook)
        self.notebook.add(members_frame, text="👥 Members")
        
        # Left side - Form
        left_frame = tk.Frame(members_frame, bg=Styles.LIGHT)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Form Card
        form_card = Styles.create_card(left_frame)
        form_card.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(form_card, text="Add New Member", font=Styles.SUBHEADING_FONT, bg=Styles.WHITE).pack(pady=10)
        
        # Form fields
        form_fields = tk.Frame(form_card, bg=Styles.WHITE)
        form_fields.pack(fill=tk.X, padx=20, pady=10)
        
        # Member ID
        tk.Label(form_fields, text="Member ID:", bg=Styles.WHITE, anchor='w').grid(row=0, column=0, sticky='w', pady=5)
        self.member_id_entry = tk.Entry(form_fields, width=20, font=Styles.NORMAL_FONT)
        self.member_id_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Name
        tk.Label(form_fields, text="Name:", bg=Styles.WHITE, anchor='w').grid(row=1, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(form_fields, width=20, font=Styles.NORMAL_FONT)
        self.name_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Phone
        tk.Label(form_fields, text="Phone:", bg=Styles.WHITE, anchor='w').grid(row=2, column=0, sticky='w', pady=5)
        self.phone_entry = tk.Entry(form_fields, width=20, font=Styles.NORMAL_FONT)
        self.phone_entry.grid(row=2, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Address
        tk.Label(form_fields, text="Address:", bg=Styles.WHITE, anchor='w').grid(row=3, column=0, sticky='w', pady=5)
        self.address_text = tk.Text(form_fields, width=20, height=3, font=Styles.NORMAL_FONT)
        self.address_text.grid(row=3, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        form_fields.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(form_card, bg=Styles.WHITE)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        Styles.create_button(button_frame, "Add Member", self.add_member, Styles.SUCCESS).pack(side=tk.LEFT, padx=(0, 10))
        Styles.create_button(button_frame, "Clear", self.clear_member_form, Styles.SECONDARY).pack(side=tk.LEFT)
        
        # Right side - Members List
        right_frame = tk.Frame(members_frame, bg=Styles.LIGHT)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # List header
        list_header = tk.Frame(right_frame, bg=Styles.LIGHT)
        list_header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(list_header, text="Members List", font=Styles.SUBHEADING_FONT, bg=Styles.LIGHT).pack(side=tk.LEFT)
        
        Styles.create_button(list_header, "Refresh", self.load_members, Styles.INFO).pack(side=tk.RIGHT)
        
        # Treeview
        tree_frame = tk.Frame(right_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Member ID', 'Name', 'Phone', 'Address', 'Created At')
        self.members_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        for col in columns:
            self.members_tree.heading(col, text=col)
        
        # Define columns
        self.members_tree.column('ID', width=50)
        self.members_tree.column('Member ID', width=100)
        self.members_tree.column('Name', width=150)
        self.members_tree.column('Phone', width=100)
        self.members_tree.column('Address', width=200)
        self.members_tree.column('Created At', width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.members_tree.yview)
        self.members_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.members_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def create_books_tab(self):
        # Books Tab
        books_frame = ttk.Frame(self.notebook)
        self.notebook.add(books_frame, text="📚 Books")
        
        # Treeview for books
        tree_frame = tk.Frame(books_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Book ID', 'Title', 'Category', 'Author', 'ISBN', 'Available', 'Total', 'Created At')
        self.books_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        for col in columns:
            self.books_tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.books_tree.yview)
        self.books_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.books_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def create_transactions_tab(self):
        # Transactions Tab
        trans_frame = ttk.Frame(self.notebook)
        self.notebook.add(trans_frame, text="📖 Transactions")
        
        # Treeview for transactions
        tree_frame = tk.Frame(trans_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Member ID', 'Book ID', 'Member', 'Book', 'Issue Date', 'Due Date', 'Return Date', 'Status')
        self.trans_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        for col in columns:
            self.trans_tree.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.trans_tree.yview)
        self.trans_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.trans_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Action buttons
        action_frame = tk.Frame(trans_frame, bg=Styles.LIGHT)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        Styles.create_button(action_frame, "Refresh", self.load_transactions, Styles.INFO).pack(side=tk.LEFT)
        Styles.create_button(action_frame, "Return Book", self.return_book, Styles.SUCCESS).pack(side=tk.LEFT, padx=(10, 0))
    
    def load_members(self):
        """Load members from database into treeview"""
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        
        members = self.db.get_all_members()
        if members:
            for member in members:
                # Truncate long addresses for display
                address = member['address']
                if len(address) > 50:
                    address = address[:50] + '...'
                
                self.members_tree.insert('', 'end', values=(
                    member['id'],
                    member['member_id'],
                    member['name'],
                    member['phone'],
                    address,
                    member['created_at']
                ))
    
    def load_books(self):
        """Load books from database into treeview"""
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        books = self.db.get_all_books()
        if books:
            for book in books:
                self.books_tree.insert('', 'end', values=(
                    book['id'],
                    book['book_id'],
                    book['title'],
                    book['category'],
                    book['author'],
                    book['isbn'] or '',
                    book['available_copies'],
                    book['total_copies'],
                    book['created_at']
                ))
    
    def load_transactions(self):
        """Load transactions from database into treeview"""
        for item in self.trans_tree.get_children():
            self.trans_tree.delete(item)
        
        transactions = self.db.get_all_transactions()
        if transactions:
            for trans in transactions:
                self.trans_tree.insert('', 'end', values=(
                    trans['id'],
                    trans['member_id'],
                    trans['book_id'],
                    trans['member_name'],
                    trans['book_title'],
                    trans['issue_date'],
                    trans['due_date'],
                    trans['return_date'] or 'Not Returned',
                    trans['status']
                ))
    
    def add_member(self):
        """Add new member to database"""
        member_id = self.member_id_entry.get().strip()
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_text.get('1.0', tk.END).strip()
        
        if not all([member_id, name, phone, address]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            result = self.db.add_member(member_id, name, address, phone)
            if result:
                messagebox.showinfo("Success", "Member added successfully!")
                self.clear_member_form()
                self.load_members()
            else:
                messagebox.showerror("Error", "Failed to add member!")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def clear_member_form(self):
        """Clear all form fields"""
        self.member_id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_text.delete('1.0', tk.END)
    
    def return_book(self):
        """Return selected book"""
        selected = self.trans_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a transaction to return!")
            return
        
        transaction_id = self.trans_tree.item(selected[0])['values'][0]
        book_title = self.trans_tree.item(selected[0])['values'][4]
        
        confirm = messagebox.askyesno("Confirm", f"Return book: {book_title}?")
        if confirm:
            try:
                result = self.db.return_book(transaction_id)
                if result:
                    messagebox.showinfo("Success", "Book returned successfully!")
                    self.load_transactions()
                    self.load_books()  # Refresh books to update available copies
                else:
                    messagebox.showerror("Error", "Failed to return book!")
            except Exception as e:
                messagebox.showerror("Error", f"Database error: {str(e)}")

def main():
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
    
    # Close database connection when app closes
    app.db.close()

if __name__ == "__main__":
    main()