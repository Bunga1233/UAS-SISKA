from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Konfigurasi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_db'

mysql = MySQL(app)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# CREATE - Tambah lagu baru
@app.route('/songs', methods=['POST'])
def add_song():
    try:
        data = request.json
        required_fields = ['judul_lagu', 'artis', 'tahun_rilis', 'durasi', 'genre']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO songs (judul_lagu, artis, tahun_rilis, durasi, genre) VALUES (%s, %s, %s, %s, %s)",
                       (data['judul_lagu'], data['artis'], data['tahun_rilis'], data['durasi'], data['genre']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Song added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ - Ambil semua lagu
@app.route('/songs', methods=['GET'])
def get_songs():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM songs")
        rows = cursor.fetchall()
        cursor.close()
        songs = [{'id': row[0], 'judul_lagu': row[1], 'artis': row[2], 'tahun_rilis': row[3],
                  'durasi': row[4], 'genre': row[5]} for row in rows]
        return jsonify(songs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET - Ambil lagu berdasarkan ID
@app.route('/songs/<int:id>', methods=['GET'])
def get_song_by_id(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM songs WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            song = {
                'id': row[0],
                'judul_lagu': row[1],
                'artis': row[2],
                'tahun_rilis': row[3],
                'durasi': row[4],
                'genre': row[5]
            }
            return jsonify(song)
        else:
            return jsonify({'message': 'Song not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE - Edit data lagu
@app.route('/songs/<int:id>', methods=['PUT'])
def update_song(id):
    try:
        data = request.json
        required_fields = ['judul_lagu', 'artis', 'tahun_rilis', 'durasi', 'genre']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE songs SET judul_lagu = %s, artis = %s, tahun_rilis = %s, durasi = %s, genre = %s WHERE id = %s",
                       (data['judul_lagu'], data['artis'], data['tahun_rilis'], data['durasi'], data['genre'], id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Song updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE - Hapus lagu
@app.route('/songs/<int:id>', methods=['DELETE'])
def delete_song(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM songs WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Song deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
