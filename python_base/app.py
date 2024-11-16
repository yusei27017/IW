from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL 配置
DB_CONFIG = {
    'host': 'dev-mysql',
    'user': 'user',
    'password': 'password',
    'database': 'mydatabase',
}

# 建立資料庫連線
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# 課程列表 API
@app.route('/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT courses.*, lecturers.name AS lecturer_name, lecturers.email AS lecturer_email, TIME_FORMAT(start_time, '%H:%i') AS start_time, TIME_FORMAT(end_time, '%H:%i') AS end_time 
                   FROM courses JOIN lecturers ON courses.lecturer_id = lecturers.id LIMIT 2
                   """)
    courses = cursor.fetchall()
    # 查看完整的查詢結果
    print(courses)

    # 或者逐行打印
    for course in courses:
        print(course)

    cursor.close()
    conn.close()
    return jsonify(courses)

# 授課講師列表 API
@app.route('/lecturers', methods=['GET'])
def get_lecturers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email FROM lecturers LIMIT 2")
    lecturers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(lecturers)

# 授課講師所開課程列表 API
@app.route('/lecturers/<int:lecturer_id>/courses', methods=['GET'])
def get_lecturer_courses(lecturer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT courses.*, TIME_FORMAT(start_time, '%H:%i') AS start_time, TIME_FORMAT(end_time, '%H:%i') AS end_time "
            "FROM courses WHERE lecturer_id = %s LIMIT 2",
            (lecturer_id,)
        )
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        if not courses:
            return jsonify({'error': 'No courses found for the given lecturer'}), 404
        return jsonify(courses), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


# 建立新講師 API
@app.route('/lecturers', methods=['POST'])
def create_lecturer():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid input, JSON body is required'}), 400
        required_fields = ['name', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO lecturers (name, email) VALUES (%s, %s)",
            (data['name'], data['email'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Lecturer created successfully'}), 201
    except KeyError as ke:
        return jsonify({'error': 'Missing or invalid input field', 'details': str(ke)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500

# 建立新課程 API
@app.route('/courses', methods=['POST'])
def create_course():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid input, JSON body is required'}), 400
        required_fields = ['course_name', 'description', 'start_time', 'end_time', 'lecturer_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO courses (course_name, description, start_time, end_time, lecturer_id) VALUES (%s, %s, %s, %s, %s)",
            (data['course_name'], data['description'], data['start_time'], data['end_time'], data['lecturer_id'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Course created successfully'}), 201

    except KeyError as ke:
        # 捕獲KeyError（字段缺失）
        return jsonify({'error': 'Missing or invalid input field', 'details': str(ke)}), 400

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500



# 更新課程內容 API
@app.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid input, JSON body is required'}), 400
        
        required_fields = ['course_name', 'description', 'start_time', 'end_time']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE courses SET course_name = %s, description = %s, start_time = %s, end_time = %s WHERE id = %s",
            (data.get('course_name'), data.get('description'), data.get('start_time'), data.get('end_time'), course_id)
        )
        if cursor.rowcount == 0:
            conn.rollback()
            cursor.close()
            conn.close()
            return jsonify({'error': 'Course not found'}), 404
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Course updated successfully'})

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


# 刪除課程 API
@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Course not found'}), 404
        conn.commit()
        cursor.close()
        conn.close()
        return '', 204  # 成功刪除返回 204 No Content
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    return "hello test"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
