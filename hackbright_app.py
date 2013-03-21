import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    #this line has to match the names of the tables exactly
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    # DB.execute requires commas even for single parameters, has to be a tuple
    DB.execute(query, (github,))
    #will fetch one row from db
    row = DB.fetchone()
    # answer is raw data from row, will include Unicode, need to use %s
    print """\    
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    #program only works with this database schema. Check to make sure filename is correct.
    CONN = sqlite3.connect("my_database.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
        query = """INSERT INTO Students values (?, ?, ?)"""
        DB.execute(query, (first_name, last_name, github))
        #CONN.commit() only require if inserting data into tables
        CONN.commit()
        print "Successfully added student: %s %s" % (first_name, last_name)

def add_new_project(title, description, max_grade):
        query = """INSERT INTO Projects values (?, ?, ?)"""
        DB.execute(query, (title, description, max_grade))
        CONN.commit()
        print "Succesfully added a new project: %s" % (title)

def get_project_by_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Description: %s
Max Grade: %s"""%(row[1], row[2])

def get_grade_by_project(github, title):
    query ="""SELECT grade FROM Grades WHERE student_github =? AND project_title=?"""
    DB.execute(query, (github, title))
    row = DB.fetchone()
    print "Grade: %s" %(row[0])

def new_grade(github, title, grade):
    query = """INSERT INTO GRADES values (?, ?, ?) """
    DB.execute(query, (github, title, grade))
    CONN.commit()
    print "Added new grade for ", github 

def all_grades(github):
    query = """SELECT project_title, grade FROM Grades WHERE student_github = ?"""
    # DB.execute requires commas even for single parameters, has to be a tuple
    DB.execute(query, (github,))
    #fetch all rows from db
    row = DB.fetchall()
    for item in row:
        print "Title: %s" % (item[0]) 
        print "Grade: %s" % (item[1])

def main():
    connect_to_db()
    command = None
    while command != ".q":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "add_project":
            add_new_project(*args)
        elif command == "get_project_by_title":
            get_project_by_title(*args)
        elif command == "new_grade":
            new_grade(*args)
        elif command == "get_grade":
            get_grade_by_project(*args)
        elif command == "all_grades":
            all_grades(*args)    

    CONN.close()

if __name__ == "__main__":
    main()
