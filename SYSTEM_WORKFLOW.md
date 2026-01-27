# Subject Enrollment Workflow Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEACHER DASHBOARD                             │
└──────────────────┬──────────────────┬──────────────────────────┘
                   │                  │
        ┌──────────▼────────┐  ┌──────▼──────────────┐
        │  Bulk Enroll      │  │  Manage Individual  │
        │  Class Subjects   │  │  Student Subjects   │
        └──────────┬────────┘  └──────┬──────────────┘
                   │                   │
        ┌──────────▼────────────────────▼─────┐
        │   enroll_subjects.py Module          │
        │  (Database Operations)               │
        └──────────┬────────────────────┬─────┘
                   │                    │
        ┌──────────▼──────┐   ┌────────▼──────────┐
        │  sqlite3        │   │  Flask Routes     │
        │  student.db     │   │  app2.py          │
        │                 │   │                   │
        │ student_subject │   │ 5 new routes      │
        │ _enrollment     │   │ 400+ lines        │
        └─────────────────┘   └───────────────────┘
```

## Data Flow - Bulk Enrollment

```
Teacher Selects Class
        │
        ▼
Load Class from teachers table
        │
        ▼
Select Subjects (Form)
        │
        ▼
POST to /enroll_class_subjects_submit
        │
        ▼
For Each Subject:
    ├─ enroll_class_in_subject(grade, subject)
    │
    ├─ Get all students in grade
    │
    └─ For Each Student:
        └─ enroll_student_subject(admission_no, subject)
           │
           ▼
        INSERT INTO student_subject_enrollment
        │
        ▼
    Store enrollment result
        │
        ▼
Redirect with Success Message
        │
        ▼
Display enrollment statistics
```

## Data Flow - Individual Student Management

```
Teacher Selects Class
        │
        ▼
get_class_enrollment_status(grade)
        │
        ├─ Join students, rest, student_subject_enrollment
        │
        └─ GROUP BY admission_no
           │
           ▼
Display Student List
(with subject count per student)
        │
        ▼
Teacher Clicks Edit on Student
        │
        ▼
get_student_enrolled_subjects(admission_no)
        │
        │
        ▼
Load Edit Form
(with checkboxes for all subjects)
        │
        ▼
Teacher Modifies Selection
        │
        ▼
POST to /save_student_subjects
        │
        ├─ Get current subjects
        │
        ├─ Get new subjects
        │
        ├─ Calculate differences
        │
        ├─ unenroll_student_subject() for removed
        │
        └─ enroll_student_subject() for added
           │
           ▼
Redirect with Success Message
```

## Database Schema

```
┌──────────────────────────────┐
│   students (existing)        │
├──────────────────────────────┤
│ admission_no (PK)            │
│ first_name                   │
│ middle_name                  │
│ last_name                    │
│ gender                       │
│ age                          │
│ email                        │
│ ...                          │
└──────┬───────────────────────┘
       │ 1
       │
       │ (FK)
       │
       │ N
┌──────▼────────────────────────────┐
│   student_subject_enrollment      │ ◄─ NEW TABLE
├───────────────────────────────────┤
│ id (PK)                           │
│ admission_no (FK → students)      │
│ subject (VARCHAR)                 │
│ enrollment_date (DATETIME)        │
│ status (active/inactive)          │
│ UNIQUE(admission_no, subject)     │
└───────────────────────────────────┘

Note: Also connected through:
┌──────────────────────────────┐
│   rest (existing)            │
├──────────────────────────────┤
│ admission_no (FK)            │
│ Grade (VARCHAR)              │
│ ...                          │
└──────────────────────────────┘
```

## API Routes Summary

| Route | Method | Purpose | Parameters |
|-------|--------|---------|------------|
| `/enroll_class_subjects` | GET/POST | Main bulk enrollment page | class_select (POST) |
| `/enroll_class_subjects_submit` | POST | Process bulk enrollment | class_id, subjects[] |
| `/manage_student_subjects` | GET/POST | View class enrollments | class_select (POST) |
| `/edit_student_subjects` | POST | Load individual edit form | admission_no, class_id |
| `/save_student_subjects` | POST | Save individual changes | admission_no, subjects[] |

## UI Components

### Page 1: Bulk Enrollment
```
┌─────────────────────────────────────────┐
│ 📚 Enroll Class in Subjects             │
├─────────────────────────────────────────┤
│                                         │
│ Select Class: [Dropdown ▼]              │
│                                         │
│ Available Subjects:                     │
│ ☐ Mathematics  ☐ Biology               │
│ ☐ Chemistry    ☐ Physics               │
│ ☐ Geography    ☐ Business              │
│ ☐ English      ☐ Kiswahili             │
│ ☐ CRE          ☐ French                │
│                                         │
│ [Enroll Class in Selected Subjects]     │
│                                         │
│ Class Enrollment Status:                │
│ ┌─────────────────────────────────────┐ │
│ │ Admission│ Name │ Enrolled Subjects│ │
│ ├─────────────────────────────────────┤ │
│ │ 001/2024 │ John │ 3 subjects  ✓   │ │
│ │ 002/2024 │ Jane │ 3 subjects  ✓   │ │
│ │ ...      │      │                 │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ← Back to Dashboard                     │
└─────────────────────────────────────────┘
```

### Page 2: Manage Individual Students
```
┌──────────────────────────────────────────┐
│ 👥 Manage Student Subjects               │
├──────────────────────────────────────────┤
│                                          │
│ Grade 1 - Student Enrollment Details     │
│ ┌──────────────────────────────────────┐ │
│ │ Admit│Student Name│Subjects │Actions│ │
│ ├──────────────────────────────────────┤ │
│ │001/24│John Doe    │Math,Eng │[Edit] │ │
│ │002/24│Jane Smith  │Bio,Chem │[Edit] │ │
│ │...   │...         │...      │...    │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ ← Back                                   │
└──────────────────────────────────────────┘
```

### Page 3: Edit Individual Student
```
┌──────────────────────────────────────────┐
│ ✏️ Edit Student Subjects                 │
├──────────────────────────────────────────┤
│                                          │
│ Student: 001/2024 - John Doe             │
│ Currently Enrolled: [Math][English]      │
│                                          │
│ Available Subjects:                      │
│ ☑ Mathematics      ☐ French              │
│ ☐ Biology          ☐ CRE                 │
│ ☑ Chemistry        ☐ Business            │
│ ☐ Physics          ☐ Kiswahili           │
│ ☐ Geography        ☑ English             │
│                                          │
│ [Save Changes]  [Cancel]                 │
│                                          │
│ ← Back                                   │
└──────────────────────────────────────────┘
```

## Access Control

```
┌─────────────────────┐
│  User Login         │
└────────┬────────────┘
         │
    ┌────▼─────┐
    │ Who?      │
    └─┬──┬──┬──┘
      │  │  │
      │  │  └─────────────┐
      │  │                │
      │  └────┐           │
      │       │           │
   Student  Manager     Teacher ◄─ Can access subject enrollment
      │       │           │
      └──┬────┴───┬───────┘
         │        │
    No   │    Yes │
    ├────┘        ├──────────────────────┐
    │             │                      │
    ▼             ▼                      ▼
Redirect    Load Home      Load Subject Enrollment
to Login                   Features with:
                          - Their assigned classes
                          - Students in those classes
                          - Available subjects
```

## Error Handling

```
Common Issues & Resolution:

1. Student Already Enrolled in Subject
   │
   └─ Handled by UNIQUE constraint
      └─ insert fails gracefully
         └─ enrollment function returns False

2. Invalid Class Selection
   │
   └─ Checked in route
      └─ Validated against class_mapping1
         └─ Flash error message if invalid

3. No Subjects Selected
   │
   └─ Form validation in route
      └─ Redirect with warning message
         └─ User prompted to select subjects

4. Session Expired / Not Logged In
   │
   └─ Check session['userName']
      └─ Redirect to login if missing
         └─ No data exposed to unauthorized users
```

## Performance Considerations

```
Operation: Enroll 30 students in 3 subjects

Execution Breakdown:
├─ POST request processing: ~10ms
├─ Query students in class: ~5ms
├─ 30 students × 3 subjects:
│  ├─ 90 INSERT operations: ~150ms
│  └─ Database commits: ~40ms
├─ Build success message: ~2ms
├─ Redirect response: ~5ms
└─ TOTAL: ~212ms (acceptable)

Optimization Notes:
- SQLite handles concurrent reads well
- Unique constraint check is O(1) with primary key
- Consider batch inserts if enrolling 1000+ students
```

