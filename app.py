from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import mysql.connector
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

# --- File Upload Config ---
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

ASSIGNMENT_FOLDER = os.path.join(app.config['UPLOAD_FOLDER'], 'assignments')
if not os.path.exists(ASSIGNMENT_FOLDER):
    os.makedirs(ASSIGNMENT_FOLDER)

# Update ALLOWED_EXTENSIONS if needed
ALLOWED_ASSIGNMENT_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

def allowed_assignment_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_ASSIGNMENT_EXTENSIONS

# --- Database connection ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="eduvault"
)
cursor = db.cursor()

# -------------------- Routes --------------------

@app.route('/')
def index():
    return render_template('index.html')

# --- Student Login ---
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM student WHERE username = %s AND password = %s", (username, password))
        student = cursor.fetchone()

        if student:
            session['student_id'] = student[0]
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid student credentials')
            
    return render_template('student/student_login.html')

# --- Teacher Login ---
@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM teacher WHERE username = %s AND password = %s", (username, password))
        teacher = cursor.fetchone()

        if teacher:
            session['teacher_id'] = teacher[0]
            session['teacher_username'] = username
            return redirect(url_for('teacher_dashboard'))
        else:
            flash('Invalid teacher credentials')
    return render_template('teacher/staff_login.html')

# --- Teacher Dashboard ---
@app.route('/teacher_dashboard', methods=['GET'])
def teacher_dashboard():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))

    cursor.execute("SELECT * FROM study_materials")
    materials = cursor.fetchall()

    cursor.execute("SELECT * FROM videos")
    videos = cursor.fetchall()

    cursor.execute("SELECT * FROM tests")
    tests = cursor.fetchall()

    cursor.execute("SELECT * FROM assignments")
    assignments = cursor.fetchall()

    teacher_id = session['teacher_id']

    cursor.execute("SELECT firstname, department FROM teacher WHERE id = %s", (teacher_id,))
    user_data = cursor.fetchone()   

    firstname = user_data[0]
    department = user_data[1]

    return render_template('/teacher/OG_UI.html', materials=materials, videos=videos, tests=tests, assignments=assignments, firstname=firstname, department=department)


# --- Upload Study Material (POST only) ---
@app.route('/upload', methods=['POST'])
def upload():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))

    if 'title' not in request.form or 'file' not in request.files:
        flash("Missing form data.")
        return redirect(url_for('teacher_dashboard'))

    title = request.form['title']
    description = request.form['description']
    file = request.files['file']

    # Debugging print statements
    print("Title:", title)
    print("Description:", description)
    print("File:", file)

    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Debugging: check if file path is correct
        print("Saving file to:", file_path)

        file.save(file_path)

        uploaded_by = session.get('teacher_username', 'Unknown')
        try:
            cursor.execute(
                "INSERT INTO study_materials (title, description, filename, uploaded_by) VALUES (%s, %s, %s, %s)",
                (title, description, unique_filename, uploaded_by)
            )
            db.commit()
            flash("Study material uploaded successfully.")
        except mysql.connector.Error as err:
            print("Error inserting into database:", err)
            flash("Error uploading study material.")
    else:
        flash("Invalid file format.")

    # Fetch all students to notify them
        cursor.execute("SELECT id FROM student")
        students = cursor.fetchall()

        # Send notifications to all students
        for student in students:
            student_id = student[0]
            message = f"New study material uploaded: {title}"
            cursor.execute(
                "INSERT INTO notifications (student_id, message) VALUES (%s, %s)",
                (student_id, message)
            )

        db.commit()

        flash("Study material uploaded successfully and notifications sent.")
    
    return redirect(url_for('teacher_dashboard'))


@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))

    if 'title' not in request.form or 'file' not in request.files:
        flash("Missing form data.")
        return redirect(url_for('teacher_dashboard'))

    title = request.form['title']
    file = request.files['file']

    if file and file.filename.endswith(('.mp4', '.mov', '.avi')):
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

        cursor.execute(
            "INSERT INTO videos (title, filename) VALUES (%s, %s)",
            (title, unique_filename)
        )
        db.commit()

        # Send notification
        cursor.execute("SELECT id FROM student")
        students = cursor.fetchall()

        for student in students:
            student_id = student[0]
            message = f"New video uploaded: {title}"
            cursor.execute("INSERT INTO notifications (student_id, message) VALUES (%s, %s)", (student_id, message))
        
        db.commit()

        flash("Video uploaded successfully and notifications sent.")
    else:
        flash("Invalid video format.")

    return redirect(url_for('teacher_dashboard'))

# --- Delete Video ---
@app.route('/delete_video/<int:video_id>')
def delete_video(video_id):
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))

    cursor.execute("SELECT filename FROM videos WHERE id = %s", (video_id,))
    video = cursor.fetchone()

    if video:
        filename = video[0]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        cursor.execute("DELETE FROM videos WHERE id = %s", (video_id,))
        db.commit()
        flash("Video deleted successfully.")
    else:
        flash("Video not found.")

    return redirect(url_for('teacher_dashboard'))


# --- Upload Test ---
@app.route('/upload_test', methods=['POST'])
def upload_test():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))

    if 'title' not in request.form or 'date' not in request.form or 'link' not in request.form:
        flash("Missing form data.")
        return redirect(url_for('teacher_dashboard'))

    title = request.form['title']
    date = request.form['date']
    link = request.form['link']

    cursor.execute(
        "INSERT INTO tests (title, date, link) VALUES (%s, %s, %s)",
        (title, date, link)
    )
    db.commit()

    # Send notification
    cursor.execute("SELECT id FROM student")
    students = cursor.fetchall()

    for student in students:
        student_id = student[0]
        message = f"New test scheduled: {title} on {date}"
        cursor.execute("INSERT INTO notifications (student_id, message) VALUES (%s, %s)", (student_id, message))

    db.commit()

    flash("Test uploaded successfully and notifications sent.")
    return redirect(url_for('teacher_dashboard'))

@app.route('/upload_assignment', methods=['POST'])
def upload_assignment():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))

    title = request.form['title']
    given_date = request.form['given_date']
    last_date = request.form['last_date']
    uploaded_by = session.get('teacher_username', 'Unknown')

    cursor.execute(
        "INSERT INTO assignments (title, given_date, last_date, uploaded_by) VALUES (%s, %s, %s, %s)",
        (title, given_date, last_date, uploaded_by)
    )
    db.commit()

    # Send notification
    cursor.execute("SELECT id FROM student")
    students = cursor.fetchall()

    for student in students:
        student_id = student[0]
        message = f"New assignment posted: {title} (Due: {last_date})"
        cursor.execute("INSERT INTO notifications (student_id, message) VALUES (%s, %s)", (student_id, message))

    db.commit()

    flash("Assignment uploaded successfully and notifications sent.")
    return redirect(url_for('teacher_dashboard'))

@app.route('/student_dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    cursor.execute("SELECT * FROM study_materials")
    materials = cursor.fetchall()

    cursor.execute("SELECT * FROM videos")
    videos = cursor.fetchall()

    cursor.execute("SELECT * FROM tests")
    tests = cursor.fetchall()

    cursor.execute("SELECT * FROM assignments")
    assignments = cursor.fetchall()

    # Fetch notifications for the logged-in student
    student_id = session['student_id']
    cursor.execute("SELECT * FROM notifications WHERE student_id = %s AND is_read = FALSE", (student_id,))
    notifications = cursor.fetchall()

    # Mark notifications as read when student views them
    cursor.execute("UPDATE notifications SET is_read = TRUE WHERE student_id = %s", (student_id,))
    db.commit()

    cursor.execute("SELECT username, department FROM student WHERE id = %s", (student_id,))
    user_data = cursor.fetchone()

    username = user_data[0]
    department = user_data[1]

    return render_template('/student/student_og_uii.html', materials=materials, videos=videos, tests=tests, assignments=assignments, notifications=notifications, username=username, department=department)

# --- Serve Uploaded Files ---
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Get form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        department = request.form['department']

        # Handle file upload (update photo)
        photo_filename = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                photo_filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        # Update profile data in the database
        cursor = db.cursor()

        if photo_filename:
            cursor.execute('''
                UPDATE teacher
                SET firstname=%s, lastname=%s, email=%s, department=%s, photo=%s
                WHERE id=1  -- Change this to use the actual teacher's ID
            ''', (firstname, lastname, email, department, photo_filename))
        else:
            cursor.execute('''
                UPDATE teacher
                SET firstname=%s, lastname=%s, email=%s, department=%s
                WHERE id=1  -- Change this to use the actual teacher's ID
            ''', (firstname, lastname, email, department))

        db.commit()  # Commit changes
        cursor.close()

        # Redirect to the same page to see updated information
        return redirect(url_for('profile'))

    # Fetch current profile data from the database
    cursor = db.cursor()
    cursor.execute('SELECT * FROM teacher WHERE id=1')  # Change to use actual teacher's ID
    teacher = cursor.fetchone()
    cursor.close()

    return render_template('/teacher/index.html', teacher=teacher)


@app.route('/profiles', methods=['GET', 'POST'])
def profiles():
    if request.method == 'POST':
        # Get form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        department = request.form['department']

        # Handle file upload (update photo)
        photo_filename = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and allowed_file(file.filename):
                photo_filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        # Update profile data in the database
        cursor = db.cursor()

        if photo_filename:
            cursor.execute('''
                UPDATE student
                SET first_name=%s, last_name=%s, email=%s, department=%s, photo=%s
                WHERE id=1  -- Change this to use the actual teacher's ID
            ''', (firstname, lastname, email, department, photo_filename))
        else:
            cursor.execute('''
                UPDATE student
                SET first_name=%s, last_name=%s, email=%s, department=%s
                WHERE id=1  -- Change this to use the actual teacher's ID
            ''', (firstname, lastname, email, department))

        db.commit()  # Commit changes
        cursor.close()

        # Redirect to the same page to see updated information
        return redirect(url_for('profiles'))

    # Fetch current profile data from the database
    cursor = db.cursor()
    cursor.execute('SELECT * FROM student WHERE id=1')  # Change to use actual teacher's ID
    student = cursor.fetchone()
    cursor.close()

    return render_template('/student/index.html', student=student)

@app.route('/upload_class_link', methods=['POST'])
def upload_class_link():
    title = request.form['title']
    link = request.form['link']
    class_time = request.form['class_time']
    uploaded_by = "teacher_username"  # Replace with session data in real usage

    
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO class_links (title, link, class_time, uploaded_by)
        VALUES (%s, %s, %s, %s)
    """, (title, link, class_time, uploaded_by))
    db.commit()
    cursor.close()
    db.close()

    return redirect('/teacher_dashboard')

@app.route('/student_class_links')
def student_class_links():
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM class_links
        WHERE class_time > NOW()
        ORDER BY class_time ASC
    """)
    links = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('/student/student_og_uii.html', links=links)


# --- Logout (both) ---
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
