# Subject Enrollment - Usage Examples & Scenarios

## Scenario 1: Grade 1 Teacher Enrolls Entire Class in Core Subjects

**Situation:** Grade 1 teacher wants to enroll all 25 students in their class for Mathematics, English, and Kiswahili.

### Steps:

1. **Login** as teacher
   - Username: `teacher_grade1`
   - Password: `****`

2. **Navigate** to "Enroll Class in Subjects"
   - Click on "Enroll Class in Subjects" button from dashboard
   - URL: `http://yoursite.com/enroll_class_subjects`

3. **Select Class**
   - Dropdown shows: "Grade 1", "Grade 2" (teacher's assigned classes)
   - Select: "Grade 1"
   - Page auto-loads showing all 25 students

4. **Select Subjects**
   ```
   ✓ Mathematics
   ✓ English
   ✓ Kiswahili
   ☐ Biology
   ☐ Chemistry
   ☐ Physics
   ☐ Geography
   ☐ Business
   ☐ CRE
   ☐ French
   ```

5. **Click** "Enroll Class in Selected Subjects"

6. **Result:** Success message appears
   ```
   "Enrollment complete. 
    Mathematics: 25 students enrolled. 
    English: 25 students enrolled. 
    Kiswahili: 25 students enrolled."
   ```

7. **Verify** in status table below
   ```
   | Admission No | Student Name      | Enrolled Subjects |
   |--------------|-------------------|-------------------|
   | 001/2024     | Alice Mwangi      | 3 subjects ✓      |
   | 002/2024     | Bob Kipchoge      | 3 subjects ✓      |
   | 003/2024     | Carol Muthoni     | 3 subjects ✓      |
   | ...          | ...               | ...               |
   | 025/2024     | Zara Ahmed        | 3 subjects ✓      |
   ```

---

## Scenario 2: Correct Enrollment for Individual Student

**Situation:** John (admission no 001/2024) was enrolled in Biology and Chemistry by mistake. Teacher wants to change to Math and Physics instead.

### Steps:

1. **Navigate** to "Manage Student Subjects"
   - Click "Manage Student Subjects" button
   - OR: `http://yoursite.com/manage_student_subjects`

2. **Select Class**
   - Dropdown: Select "Grade 1"
   - Page loads all students with current enrollments

3. **View Current Status**
   ```
   | Admission | Student     | Enrolled Subjects      | Actions |
   |-----------|-------------|------------------------|---------|
   | 001/2024  | John Okonkwo| Bio, Chem ✗            | [Edit]  |
   | 002/2024  | Jane Smith  | Math, Eng, Kiswahili   | [Edit]  |
   ```

4. **Click [Edit]** on John's row

5. **Edit Screen Appears**
   ```
   Student: 001/2024 - John Okonkwo
   Currently Enrolled: [Biology][Chemistry]
   
   Available Subjects:
   ☑ Mathematics         ☐ French
   ☐ Biology            ☐ CRE
   ☐ Chemistry          ☐ Business
   ☑ Physics            ☐ Kiswahili
   ☐ Geography          ☐ English
   ```

6. **Modify Selections**
   - Uncheck: Biology, Chemistry
   - Check: Mathematics, Physics
   
   ```
   ☑ Mathematics         ☐ French
   ☐ Biology            ☐ CRE
   ☐ Chemistry          ☐ Business
   ☑ Physics            ☐ Kiswahili
   ☐ Geography          ☐ English
   ```

7. **Click** "Save Changes"

8. **Confirmation** appears
   ```
   ✓ "Subject enrollment updated successfully"
   ```

9. **Return** to Manage Page
   ```
   | Admission | Student     | Enrolled Subjects      | Actions |
   |-----------|-------------|------------------------|---------|
   | 001/2024  | John Okonkwo| Math, Physics ✓        | [Edit]  |
   ```

---

## Scenario 3: Complex Grade-Level Enrollment

**Situation:** Grade 9 teacher needs to:
- Enroll entire class in mandatory subjects: Math, English
- Enroll different subsets in optional subjects

### Solution - Two Step Process:

**Step 1: Bulk enrollment for mandatory subjects**
1. Navigate to "Enroll Class in Subjects"
2. Select "Grade 9"
3. Check only: Mathematics, English
4. Click "Enroll"
5. Result: All 35 Grade 9 students now have Math + English

**Step 2: Individual adjustments for optional subjects**
1. Navigate to "Manage Student Subjects"
2. Select "Grade 9"
3. Edit select students:
   - STEM track students: Add Physics, Chemistry
   - Business track students: Add Business, Geography
   - Arts track students: Add History, CRE

---

## Scenario 4: Late Student Enrollment

**Situation:** New student just admitted with admission no 045/2024, needs to be enrolled in subjects.

### Steps:

1. Ensure student record exists in `students` table
2. Ensure grade is set in `rest` table (e.g., Grade 3)
3. Navigate to "Manage Student Subjects"
4. Select "Grade 3"
5. Look for new student in list (if not visible, refresh page)
6. Click [Edit]
7. Select all required subjects
8. Save

**Result:** New student now shows "3 subjects ✓" in enrollment status

---

## Scenario 5: Teacher Changes Class Assignment

**Situation:** Teacher previously taught Grade 2, now teaches Grade 5.

### Admin Action:
1. Update `teachers` table: Change `grade` column from "4,5" to "13" (Grade 5 code)

### Teacher Now Sees:
- "Enroll Class in Subjects" - only shows Grade 5
- "Manage Student Subjects" - only shows Grade 5 students
- Cannot access Grade 2 enrollments anymore

---

## Scenario 6: Data Verification & Auditing

**Situation:** School admin wants to verify subject enrollment compliance.

### Queries Available:

**All enrollments in one subject:**
```sql
SELECT s.admission_no, s.first_name, s.last_name, sse.enrollment_date
FROM student_subject_enrollment sse
JOIN students s ON sse.admission_no = s.admission_no
WHERE sse.subject = 'Mathematics' 
  AND sse.status = 'active'
ORDER BY sse.enrollment_date;
```

**Students not enrolled in required subject:**
```sql
SELECT s.admission_no, s.first_name, s.last_name
FROM students s
JOIN rest r ON s.admission_no = r.admission_no
WHERE r.Grade = 'grade1'
  AND s.admission_no NOT IN (
      SELECT admission_no FROM student_subject_enrollment 
      WHERE subject = 'Mathematics' AND status = 'active'
  );
```

**Enrollment summary by grade:**
```sql
SELECT r.Grade, 
       COUNT(DISTINCT s.admission_no) as total_students,
       COUNT(DISTINCT sse.admission_no) as enrolled_in_any_subject,
       COUNT(DISTINCT sse.subject) as subjects_offered
FROM students s
JOIN rest r ON s.admission_no = r.admission_no
LEFT JOIN student_subject_enrollment sse ON s.admission_no = sse.admission_no
WHERE sse.status = 'active'
GROUP BY r.Grade;
```

---

## Common Workflows

### Workflow A: Beginning of Term Setup
```
1. Login as teacher
2. Go to "Enroll Class in Subjects"
3. For each of my classes:
   a. Select class
   b. Check mandatory subjects
   c. Click enroll
4. Navigate to "Manage Student Subjects"
5. Do individual customizations as needed
6. Verify all students have subjects
```

**Time Estimate:** 15-30 minutes for 3 classes

### Workflow B: Mid-Term Adjustments
```
1. Student requests subject change
2. Go to "Manage Student Subjects"
3. Select student's class
4. Find student and click [Edit]
5. Adjust subject selection
6. Save
7. Inform student of confirmation
```

**Time Estimate:** 2-3 minutes per student

### Workflow C: Report Generation
```
1. Admin queries database
2. Export results to CSV
3. Share with teachers for verification
4. Teachers make corrections using interfaces
```

---

## Dashboard Integration Example

When you add these to your teacher dashboard, it could look like:

```
╔════════════════════════════════════════════════════════════════════╗
║                    TEACHER DASHBOARD                              ║
║                    Welcome, Mr. John Mwangi                        ║
╚════════════════════════════════════════════════════════════════════╝

┌─ QUICK ACTIONS ────────────────────────────────────────────────────┐
│                                                                     │
│  📊 View Marks        📅 Attendance        💬 Messages             │
│     [Open]               [Open]              [4 new]               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─ SUBJECT MANAGEMENT ───────────────────────────────────────────────┐
│                                                                     │
│  📚 Enroll Class in Subjects                                       │
│     Quickly enroll entire classes in subjects                      │
│     [→ Go to Bulk Enrollment]                                      │
│                                                                     │
│  👥 Manage Student Subjects                                        │
│     Adjust subjects for individual students                        │
│     [→ Manage Students]                                            │
│                                                                     │
│  📋 View Enrollment Report                                         │
│     See all enrollments for your classes                           │
│     [→ View Report]                                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─ MY CLASSES ──────────────────────────────────────────────────────┐
│                                                                    │
│  Grade 1  (25 students, 3 subjects assigned)   [Manage]          │
│  Grade 5  (28 students, 4 subjects assigned)   [Manage]          │
│  Grade 9  (30 students, 5 subjects assigned)   [Manage]          │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

