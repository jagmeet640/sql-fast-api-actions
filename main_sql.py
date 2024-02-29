import pymysql.cursors
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# MySQL database connection parameters
connection = pymysql.connect(
    host="jagmeet-test.cng8a4c6ag26.us-east-1.rds.amazonaws.com",
    user='admin',
    password='RAENai2024',
    database='jagmeet_etl',
    port = 3306,
    cursorclass=pymysql.cursors.DictCursor
)

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    marks: int
    rollId: int

@app.post("/students/")
def create_student(student: Student):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO students (name, age, marks, rollId) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (student.name, student.age, student.marks, student.rollId))
            print(cursor)
            connection.commit()
        return student
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.get("/students_read/")
def read_all():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM students"
            cursor.execute(sql, ())
            student = cursor.fetchall()
            if not student:
                raise HTTPException(status_code=404, detail="Student not found")
            return student
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/students/{rollId}")
def read_student(rollId: int):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM students WHERE rollId = %s"
            cursor.execute(sql, (rollId,))
            student = cursor.fetchone()
            if not student:
                raise HTTPException(status_code=404, detail="Student not found")
            return student
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/students_update/")
def update_student(student: Student):
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE students SET name=%s, age=%s, marks=%s WHERE rollId=%s"
            cursor.execute(sql, (student.name, student.age, student.marks, student.rollId))
            connection.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/students/{rollId}")
def delete_student(rollId: int):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM students WHERE rollId = %s"
            cursor.execute(sql, (rollId,))
            connection.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
