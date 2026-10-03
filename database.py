"""
Database connection and initialization module
"""

import sqlite3
from datetime import datetime
import os

class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self, db_name='library_system.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def connect(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.row_factory = sqlite3.Row
            print(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
    
    def init_database(self):
        """Initialize database tables"""
        self.connect()
        
        # Create tables
        self.cursor.executescript("""
            -- BookCategory Table
            CREATE TABLE IF NOT EXISTS book_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Book Table
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT,
                publication_year INTEGER,
                category_id INTEGER NOT NULL,
                quantity_total INTEGER NOT NULL DEFAULT 1,
                quantity_available INTEGER NOT NULL DEFAULT 1,
                location_shelf TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES book_categories(id)
            );
            
            -- Student Table
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                admission_number TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                form INTEGER NOT NULL,
                stream TEXT,
                date_of_birth TEXT,
                phone_number TEXT,
                parents_contact TEXT,
                address TEXT,
                fine_balance REAL DEFAULT 0,
                account_status TEXT DEFAULT 'active',
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Staff Table
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_id TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                role TEXT NOT NULL,
                department TEXT,
                phone_number TEXT,
                email TEXT,
                hire_date TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- BorrowingRecord Table
            CREATE TABLE IF NOT EXISTS borrowing_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                borrowed_by INTEGER NOT NULL,
                borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TEXT NOT NULL,
                return_date TIMESTAMP,
                returned_by INTEGER,
                status TEXT DEFAULT 'borrowed',
                notes TEXT,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (borrowed_by) REFERENCES staff(id),
                FOREIGN KEY (returned_by) REFERENCES staff(id)
            );
            
            -- FineRecord Table
            CREATE TABLE IF NOT EXISTS fine_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                borrowing_record_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                reason TEXT,
                status TEXT DEFAULT 'pending',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                paid_date TIMESTAMP,
                paid_by TEXT,
                FOREIGN KEY (borrowing_record_id) REFERENCES borrowing_records(id),
                FOREIGN KEY (student_id) REFERENCES students(id)
            );
            
            -- User/Login Table
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                staff_id INTEGER,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (staff_id) REFERENCES staff(id)
            );
            
            -- LibrarySettings Table
            CREATE TABLE IF NOT EXISTS library_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                school_name TEXT,
                school_email TEXT,
                school_phone TEXT,
                borrow_limit INTEGER DEFAULT 5,
                borrow_duration INTEGER DEFAULT 14,
                fine_per_day REAL DEFAULT 500,
                max_fine REAL DEFAULT 10000,
                max_overdue_days INTEGER DEFAULT 30,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Create indices for better performance
            CREATE INDEX IF NOT EXISTS idx_book_isbn ON books(isbn);
            CREATE INDEX IF NOT EXISTS idx_book_title ON books(title);
            CREATE INDEX IF NOT EXISTS idx_student_id ON students(student_id);
            CREATE INDEX IF NOT EXISTS idx_student_admission ON students(admission_number);
            CREATE INDEX IF NOT EXISTS idx_borrow_student ON borrowing_records(student_id);
            CREATE INDEX IF NOT EXISTS idx_borrow_book ON borrowing_records(book_id);
            CREATE INDEX IF NOT EXISTS idx_borrow_status ON borrowing_records(status);
            CREATE INDEX IF NOT EXISTS idx_fine_student ON fine_records(student_id);
            CREATE INDEX IF NOT EXISTS idx_fine_status ON fine_records(status);
        """)
        
        self.conn.commit()
        self.insert_default_data()
    
    def insert_default_data(self):
        """Insert default categories and settings"""
        try:
            # Check if categories exist
            self.cursor.execute("SELECT COUNT(*) FROM book_categories")
            if self.cursor.fetchone()[0] == 0:
                categories = [
                    ('Fiction', 'Fictional books and novels', 'FIC'),
                    ('Science', 'Science and research books', 'SCI'),
                    ('Mathematics', 'Mathematics textbooks', 'MATH'),
                    ('History', 'History and social studies', 'HIST'),
                    ('Literature', 'Literature and language', 'LIT'),
                    ('Reference', 'Reference materials', 'REF')
                ]
                self.cursor.executemany(
                    "INSERT INTO book_categories (name, description, code) VALUES (?, ?, ?)",
                    categories
                )
                self.conn.commit()
            
            # Check if default user exists
            self.cursor.execute("SELECT COUNT(*) FROM users")
            if self.cursor.fetchone()[0] == 0:
                # Create default admin staff
                self.cursor.execute("""
                    INSERT INTO staff (staff_id, first_name, last_name, role, department, phone_number, email, hire_date, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, ('ADMIN001', 'Admin', 'User', 'admin', 'Library', '+256700000000', 'admin@school.ug', datetime.now().strftime('%Y-%m-%d'), 1))
                
                staff_id = self.cursor.lastrowid
                
                # Create default admin user (password: admin123)
                self.cursor.execute("""
                    INSERT INTO users (username, password, role, staff_id, is_active)
                    VALUES (?, ?, ?, ?, ?)
                """, ('admin', 'admin123', 'admin', staff_id, 1))
                
                self.conn.commit()
            
            # Check if settings exist
            self.cursor.execute("SELECT COUNT(*) FROM library_settings")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    INSERT INTO library_settings (school_name, school_email, school_phone, borrow_limit, borrow_duration, fine_per_day, max_fine, max_overdue_days)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ('Secondary School', 'school@example.ug', '+256700000000', 5, 14, 500, 10000, 30))
                self.conn.commit()
        
        except sqlite3.IntegrityError:
            pass  # Data already exists
    
    def execute_query(self, query, params=None):
        """Execute a query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor
        except sqlite3.Error as e:
            print(f"Query error: {e}")
            return None
    
    def fetch_one(self, query, params=None):
        """Fetch one result"""
        cursor = self.execute_query(query, params)
        return cursor.fetchone() if cursor else None
    
    def fetch_all(self, query, params=None):
        """Fetch all results"""
        cursor = self.execute_query(query, params)
        return cursor.fetchall() if cursor else []
    
    def insert(self, query, params):
        """Insert data"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Insert error: {e}")
            self.conn.rollback()
            return None
    
    def update(self, query, params):
        """Update data"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"Update error: {e}")
            self.conn.rollback()
            return 0
    
    def delete(self, query, params):
        """Delete data"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"Delete error: {e}")
            self.conn.rollback()
            return 0
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
