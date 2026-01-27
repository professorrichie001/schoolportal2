"""
Module for managing student subject enrollment by teachers
"""
import sqlite3
import database

# Subject mapping - Complete list of all available subjects
AVAILABLE_SUBJECTS = ['Mathematics', 'English', 'Kiswahili', 'Science', 'Social Studies', 
                      'Biology', 'Chemistry', 'Physics', 'Geography', 'History', 'Civics',
                      'CRE', 'Business', 'French', 'Music', 'Computer Studies', 
                      'Physical Education', 'Arts', 'Agriculture', 'Home Science', 'Entrepreneurship']

# CBC Class to Available Subjects Mapping (Kenya Curriculum)
# Based on Kenya's official Competency-Based Curriculum standards
CLASS_SUBJECTS_MAPPING = {
    # Early Years Foundation - Integrated Learning
    'Play group': ['English', 'Kiswahili', 'Mathematics', 'Science', 'Music', 'Physical Education', 'Arts'],
    'PP1': ['English', 'Kiswahili', 'Mathematics', 'Science', 'Music', 'Physical Education', 'Arts'],
    'PP2': ['English', 'Kiswahili', 'Mathematics', 'Science', 'Music', 'Physical Education', 'Arts'],
    
    # Lower Primary - Integrated Subjects
    'Grade 1': ['English', 'Kiswahili', 'Mathematics', 'Science', 'Social Studies', 'Music', 'Physical Education', 'Arts'],
    'Grade 2': ['English', 'Kiswahili', 'Mathematics', 'Science', 'Social Studies', 'Music', 'Physical Education', 'Arts'],
    'Grade 3': ['English', 'Kiswahili', 'Mathematics', 'Science', 'Social Studies', 'Computer Studies', 'Music', 'Physical Education', 'Arts'],
    
    # Upper Primary - Introduction to Sciences & Humanities
    'Grade 4': ['English', 'Kiswahili', 'Mathematics', 'Science', 'Social Studies', 'Computer Studies', 'Agriculture', 'Home Science', 'Music', 'Physical Education', 'Arts', 'Entrepreneurship'],
    'Grade 5': ['English', 'Kiswahili', 'Mathematics', 'Science', 'Social Studies', 'Computer Studies', 'Agriculture', 'Home Science', 'Music', 'Physical Education', 'Arts', 'Entrepreneurship'],
    'Grade 6': ['English', 'Kiswahili', 'Mathematics', 'Science', 'Social Studies', 'Computer Studies', 'Agriculture', 'Home Science', 'Music', 'Physical Education', 'Arts', 'Entrepreneurship'],
    
    # Junior Secondary - Full Subject Specialization
    'Grade 7': ['English', 'Kiswahili', 'Mathematics', 'Biology', 'Chemistry', 'Physics', 'Geography', 'History', 'Civics', 'CRE', 'Business', 'Computer Studies', 'Agriculture', 'Home Science', 'Music', 'Physical Education', 'Arts', 'Entrepreneurship', 'French'],
    'Grade 8': ['English', 'Kiswahili', 'Mathematics', 'Biology', 'Chemistry', 'Physics', 'Geography', 'History', 'Civics', 'CRE', 'Business', 'Computer Studies', 'Agriculture', 'Home Science', 'Music', 'Physical Education', 'Arts', 'Entrepreneurship', 'French'],
    'Grade 9': ['English', 'Kiswahili', 'Mathematics', 'Biology', 'Chemistry', 'Physics', 'Geography', 'History', 'Civics', 'CRE', 'Business', 'Computer Studies', 'Agriculture', 'Home Science', 'Music', 'Physical Education', 'Arts', 'Entrepreneurship', 'French'],
    
    # Senior Secondary - Full Specialization with Electives
    'Grade 10': ['English', 'Kiswahili', 'Mathematics', 'Biology', 'Chemistry', 'Physics', 'Geography', 'History', 'Civics', 'CRE', 'Business', 'Computer Studies', 'Agriculture', 'Home Science', 'Music', 'Physical Education', 'Arts', 'Entrepreneurship', 'French'],
    'Grade 11': ['English', 'Kiswahili', 'Mathematics', 'Biology', 'Chemistry', 'Physics', 'Geography', 'History', 'Civics', 'CRE', 'Business', 'Computer Studies', 'Agriculture', 'Home Science', 'Music', 'Physical Education', 'Arts', 'Entrepreneurship', 'French'],
    'Grade 12': ['English', 'Kiswahili', 'Mathematics', 'Biology', 'Chemistry', 'Physics', 'Geography', 'History', 'Civics', 'CRE', 'Business', 'Computer Studies', 'Agriculture', 'Home Science', 'Music', 'Physical Education', 'Arts', 'Entrepreneurship', 'French']
}

# Subject codes for database storage
SUBJECT_CODES = {
    'Mathematics': 'math',
    'English': 'eng',
    'Kiswahili': 'kiswahili',
    'Science': 'science',
    'Social Studies': 'social',
    'Biology': 'bio',
    'Chemistry': 'chem',
    'Physics': 'phys',
    'Geography': 'geo',
    'History': 'hist',
    'Civics': 'civics',
    'CRE': 'cre',
    'Business': 'bus',
    'French': 'french',
    'Music': 'music',
    'Computer Studies': 'computer',
    'Physical Education': 'pe',
    'Arts': 'arts',
    'Agriculture': 'agri',
    'Home Science': 'homesci',
    'Entrepreneurship': 'entrep'
}

def init_student_subject_enrollment_table():
    """Create table to track student subject enrollment"""
    with sqlite3.connect('student.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_subject_enrollment(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admission_no TEXT,
            subject TEXT,
            year TEXT,
            enrollment_date DATETIME,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (admission_no) REFERENCES students (admission_no),
            UNIQUE(admission_no, subject, year)
        )
        ''')
        conn.commit()


def enroll_student_subject(admission_no, subject, year):
    """Enroll a single student in a subject for a specific year"""
    with sqlite3.connect('student.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO student_subject_enrollment (admission_no, subject, year, enrollment_date, status)
            VALUES (?, ?, ?, DATETIME('now'), 'active')
            ''', (admission_no, subject, year))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Student already enrolled in this subject for this year
            return False


def enroll_class_in_subject(grade, subject, year):
    """
    Enroll all students in a class/grade for a specific subject
    
    Args:
        grade: The grade/class code (e.g., 'grade1', 'grade12')
        subject: The subject name (e.g., 'Mathematics')
        year: The academic year (e.g., '2026')
    
    Returns:
        Dictionary with enrollment results
    """
    with sqlite3.connect('student.db') as conn:
        cursor = conn.cursor()
        
        # Get class name for this grade
        cursor.execute('SELECT DISTINCT Grade FROM rest WHERE Grade = ?', (grade,))
        class_result = cursor.fetchone()
        if not class_result:
            return {
                'total_students': 0,
                'enrolled': 0,
                'already_enrolled': 0,
                'error': 'Class not found'
            }
        
        class_name = class_result[0]
        
        # Validate subject is allowed for this class
        if not is_subject_valid_for_class(class_name, subject):
            return {
                'total_students': 0,
                'enrolled': 0,
                'already_enrolled': 0,
                'error': f'{subject} is not available for {class_name}'
            }
        
        # Get all students in the specified grade
        cursor.execute('''
        SELECT admission_no FROM rest WHERE Grade = ?
        ''', (grade,))
        
        students = cursor.fetchall()
        enrolled_count = 0
        failed_count = 0
        
        for student in students:
            admission_no = student[0]
            if enroll_student_subject(admission_no, subject, year):
                enrolled_count += 1
            else:
                failed_count += 1
        
        return {
            'total_students': len(students),
            'enrolled': enrolled_count,
            'already_enrolled': failed_count
        }

def get_student_enrolled_subjects(admission_no, year):
    """Get all subjects a student is enrolled in for a specific year"""
    with sqlite3.connect('student.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT subject, enrollment_date FROM student_subject_enrollment
        WHERE admission_no = ? AND year = ? AND status = 'active'
        ORDER BY enrollment_date
        ''', (admission_no, year))
        
        results = cursor.fetchall()
        return [result[0] for result in results]


def get_class_enrollment_status(grade, year):
    """
    Get enrollment status for all students in a class for a specific year
    
    Args:
        grade: The grade/class code
        year: The academic year
    
    Returns:
        List of tuples (admission_no, first_name, last_name, enrolled_subjects_count)
    """
    with sqlite3.connect('student.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT s.admission_no, s.first_name, s.last_name, COUNT(se.subject) as subject_count
        FROM students s
        INNER JOIN rest r ON s.admission_no = r.admission_no
        LEFT JOIN student_subject_enrollment se ON s.admission_no = se.admission_no AND se.year = ? AND se.status = 'active'
        WHERE r.Grade = ?
        GROUP BY s.admission_no
        ORDER BY s.first_name, s.last_name
        ''', (year, grade))
        
        return cursor.fetchall()


def get_subject_enrollment_for_class(grade, subject, year):
    """
    Get students in a class who are enrolled in a specific subject for a specific year
    
    Args:
        grade: The grade/class code
        subject: The subject name
        year: The academic year
    
    Returns:
        List of tuples (admission_no, first_name, last_name)
    """
    with sqlite3.connect('student.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT s.admission_no, s.first_name, s.last_name
        FROM students s
        INNER JOIN rest r ON s.admission_no = r.admission_no
        INNER JOIN student_subject_enrollment se ON s.admission_no = se.admission_no
        WHERE r.Grade = ? AND se.subject = ? AND se.year = ? AND se.status = 'active'
        ORDER BY s.first_name, s.last_name
        ''', (grade, subject, year))
        
        return cursor.fetchall()


def unenroll_student_subject(admission_no, subject, year):
    """Unenroll a student from a subject for a specific year"""
    with sqlite3.connect('student.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE student_subject_enrollment SET status = 'inactive'
        WHERE admission_no = ? AND subject = ? AND year = ?
        ''', (admission_no, subject, year))
        conn.commit()
        return cursor.rowcount > 0


def get_students_in_class(grade):
    """Get all students in a specific class/grade"""
    with sqlite3.connect('student.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT s.admission_no, s.first_name, s.last_name
        FROM students s
        INNER JOIN rest r ON s.admission_no = r.admission_no
        WHERE r.Grade = ?
        ORDER BY s.first_name, s.last_name
        ''', (grade,))
        
        return cursor.fetchall()


def get_class_available_subjects(class_name):
    """Get available subjects for a specific class according to Kenya CBC"""
    return CLASS_SUBJECTS_MAPPING.get(class_name, AVAILABLE_SUBJECTS)


def is_subject_valid_for_class(class_name, subject):
    """Check if a subject is valid/available for a specific class"""
    available = get_class_available_subjects(class_name)
    return subject in available

