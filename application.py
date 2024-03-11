import psycopg2

#Connecting to database
def connection():
    try:
        connection = psycopg2.connect(host="localhost", database="students", user="postgres", password="postgres", port="5432")
        cursor = connection.cursor()
        return connection, cursor
    except:
        print("Error connecting to Database!")

#main function
def main():
    print("Input your number (0 - 4):")
    print("0. To quit application")
    print("1. Get all of the students")
    print("2. Add new student to the database")
    print("3. Update a student's email from the database")
    print("4. Delete a student from the database")

    while True:
        try: 
            options = int(input("What is your options: \n"))
            if options == 0:
                quit()
                print("Quitting...")
                return
            elif options == 1:
                getAllStudents()
            elif options == 2:
                first_name = input("What is the student's first name: \n")
                last_name = input("What is the student's last name: \n")
                email = input("What is the student's email address: \n")
                enrollment_date = input("What is the student's enrollment date (YYYY-MM-DD): \n")
                addStudent(first_name, last_name, email, enrollment_date)
            elif options == 3:
                student_id = input("What is the student's id you want to update: \n")    
                email = input("What is the new email: \n")
                updateStudentEmail(student_id, email)
            elif options == 4:
                student_id = input("What is the student's id you want to delete: \n")
                deleteStudent(student_id)

            else:
                print("Invalid options, please try again")
            
        except:
            print("Error running loop")

# Get all students records
def getAllStudents():
    conn, cursor = connection()

    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        for student in students:
            print(student)
    except:
        print("Error getting data from students database")
    finally:
        cursor.close()
        conn.close()

#Add new student to the database
def addStudent(first_name, last_name, email, enrollment_date):
    conn, cursor = connection()

    try: 
        cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, enrollment_date))
        conn.commit()
        print("Sucessfully added new student")
    except:
        print("Error adding new student to students database")
    finally:
        cursor.close()
        conn.close()

#Update a student email
def updateStudentEmail(student_id, new_email):
    conn, cursor = connection()

    try: 
        cursor.execute("UPDATE students SET email = %s WHERE student_id = %s", (new_email, student_id))
        conn.commit()
        print("Sucessfully update email")
    except:
        print("Error updating email to students database")
    finally:
        cursor.close()
        conn.close()

#Delete a student
def deleteStudent(student_id):
    conn, cursor = connection()

    try: 
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id))
        conn.commit()
        print("Sucessfully delete student!")
    except:
        print("Error deleting student from students database")
    finally:
        cursor.close()
        conn.close()

#Quit and reset the database
def quit():
    conn, cursor = connection()
    schema = '''CREATE TABLE students (
        student_id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        enrollment_date DATE
    );'''

    original_data = [
            ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
            ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
            ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')
        ]
    try: 
        cursor.execute("DROP TABLE IF EXISTS students")
        cursor.execute(schema)
        cursor.executemany("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)", original_data)
        conn.commit()
    except:
        print("Error quitting")
    finally:
        cursor.close()
        conn.close()

main()




