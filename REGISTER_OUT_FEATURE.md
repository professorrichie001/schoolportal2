# Student Register Out (Checkout) Feature

## Overview
The Register Out feature allows teachers to track when students leave the school. This complements the Register In (attendance check-in) system by recording both arrival and departure times.

## Database Changes

### Updated attendance table
- Added `time_out` column to track checkout times
- Maintains backward compatibility with existing data
- Schema:
  ```
  attendance:
  - id (PRIMARY KEY)
  - admission_no
  - date
  - time_in
  - time_out (NEW)
  - status
  - marked_by
  ```

## Backend Implementation

### New Database Functions (database.py)

1. **`mark_student_checkout(admission_no, date, time_out)`**
   - Records when a student checks out
   - Updates the time_out field in the attendance record

2. **`get_checkout_status(admission_no, date)`**
   - Retrieves both check-in and check-out times for a student
   - Returns tuple: (time_in, time_out)

3. **`get_todays_checkouts(date)`**
   - Gets all students who have checked out on a specific date
   - Returns list of checkout records

### New Flask Routes (app2.py)

1. **GET `/register_out`**
   - Renders the student checkout page
   - Requires teacher authentication
   - Shows:
     - QR code scanner for checkout
     - Manual admission number entry
     - List of students checked out today

2. **POST `/mark_checkout`**
   - Processes student checkout requests
   - Validates:
     - Student exists
     - Student checked in today
     - Student hasn't already checked out
   - Returns: Student name, check-in time, check-out time, grade

3. **GET `/get_todays_checkouts`**
   - Returns all students who checked out today
   - Used to populate the checkout list on page load

## Frontend Implementation

### New Template: register_out.html
**Features:**
- Python-based QR code scanner (consistent with Register In)
- Manual entry mode for admission numbers
- Real-time camera feed display
- Live list of checked-out students
- Responsive design matching the attendance page

**Two Modes:**
1. **QR Scanner Mode**
   - Scans student QR codes every 500ms
   - Automatically marks checkout on detection
   - Shows live camera feed

2. **Manual Entry Mode**
   - Type admission number directly
   - Press Enter or click "Mark Checkout" button

### UI Elements
- Green color scheme (distinguishes from blue Register In)
- Icons: door-open for checkout, checkmark-circle for check-in
- Shows check-in and check-out times
- Displays student grade and admission number

## Navigation

### Sidebar Menu Links
- **Register In**: `{{ url_for('attendance') }}` - Blue checkmark icon
- **Register Out**: `{{ url_for('register_out') }}` - Green door icon

Added to:
- admin_dashboard.html
- teachers_dashboard.html

## How to Use

### Teacher Workflow
1. Log in to the portal
2. Click "Register Out" in the sidebar
3. Choose scanning mode:
   - **QR Code**: Students present their QR codes
   - **Manual**: Type admission numbers manually
4. System validates and records checkout time
5. Checked-out students appear in the list below

### Student Data Flow
1. Student scans QR or enters admission number
2. System verifies:
   - Student exists
   - Student is present (has time_in)
   - Student hasn't already checked out
3. Checkout time recorded
4. Student added to "Checked Out" list
5. Next student can check out

## Technical Specifications

### Checkout Constraints
- Student must have checked in (time_in must exist)
- Cannot checkout twice (time_out must be NULL)
- Checkout time recorded automatically from server time
- One unique attendance record per student per day

### Data Validation
- Admission number verification
- Date validation (defaults to current date)
- Time_in existence check
- Duplicate checkout prevention

### Error Handling
- Student not found: Returns error message
- Not checked in: Prevents checkout
- Already checked out: Prevents duplicate checkout
- Server errors: Logged and user-friendly message returned

## Response Format

### Success Response (mark_checkout)
```json
{
  "success": true,
  "message": "Student Name checked out",
  "student_name": "Student Name",
  "grade": "Grade/Class",
  "time_in": "HH:MM:SS",
  "time_out": "HH:MM:SS"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description"
}
```

## Integration with Existing System

### Compatible With
- Python QR Scanner (shares same `/scan_qr_python` endpoint)
- Existing attendance database schema
- Current authentication system
- Admin and teacher dashboards

### Database Migration
- Existing attendance records compatible
- `time_out` field is NULL for old records
- No data loss on upgrade
- Automatic column addition on first run

## Future Enhancements

Possible additions:
- Attendance reports showing duration (check-in to check-out)
- Alerts for students who don't check out
- Summary statistics for daily checkout rates
- Export reports with entry/exit times
- Parent notifications on student checkout
- Late checkout tracking

## Troubleshooting

**QR Scanner not working:**
- Check camera permissions
- Verify Python environment has cv2 and pyzbar
- Check server logs for errors

**Checkout fails:**
- Verify student checked in first
- Ensure admission number format is correct
- Check database has time_out column (run database initialization)

**Duplicate checkouts:**
- Page shows previous checkout prevents new ones
- Clear cache if persisting
- Check database records directly
