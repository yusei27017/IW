import requests

def insert_lect_data():
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    res = requests.post('http://127.0.0.1:5000/lecturers',json=data)
    return res

def insert_courses_data():
    data = {
        "course_name": "Introduction to Data Science",
        "description": "Learn the basics of data science and analysis.",
        "start_time": "01:00",
        "end_time": "02:00",
        "lecturer_id": 1 
    }

    res= requests.post('http://127.0.0.1:5000/courses', json=data)

    return res

def del_courses():
    course_id = 1
    res = requests.delete(f'http://127.0.0.1:5000/courses/{course_id}')
    return res

if __name__ == "__main__":
    print(del_courses())

