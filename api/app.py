import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

DB_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DB_URL)

@app.route('/bookmarks', methods=['GET', 'POST'])
def manage_bookmarks():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # handle incoming new bookmarks
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        url = data.get('url')
        page_id = data.get('page_id', 1)

        cur.execute('INSERT INTO bookmarks (title, url, page_id) VALUES (%s, %s, %s)',
                   (title, url, page_id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 'added'}), 201

    # handle retrieving bookmarks filtered by page_id
    page_id = request.args.get('page_id')
    if page_id:
        cur.execute('SELECT id, title, url FROM bookmarks WHERE page_id = %s;', (page_id,))
    else:
        cur.execute('SELECT id, title, url, page_id FROM bookmarks;')

    rows = cur.fetchall()
    if page_id:
        bookmarks = [{'id': row[0], 'title': row[1], 'url': row[2]} for row in rows]
    else:
        bookmarks = [{'id': row[0], 'title': row[1], 'url': row[2], 'page_id': row[3]} for row in rows]

    cur.close()
    conn.close()
    return jsonify(bookmarks)


@app.route('/pages', methods=['GET', 'POST'])
def manage_pages():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        cur.execute('INSERT INTO pages (name) VALUES (%s) RETURNING id, name;', (name,))
        new = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'id': new[0], 'name': new[1]}), 201

    # get pages
    cur.execute('SELECT id, name FROM pages ORDER BY id;')
    pages = [{'id': row[0], 'name': row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(pages)


@app.route('/pages/<int:page_id>', methods=['DELETE'])
def delete_page(page_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM pages WHERE id = %s RETURNING id;', (page_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return jsonify({'status': 'deleted'}), 200
    else:
        return jsonify({'status': 'not found'}), 404


@app.route('/bookmarks/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # delete the bookmark with the given id
    cur.execute('DELETE FROM bookmarks WHERE id = %s RETURNING id;', (bookmark_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return jsonify({'status': 'deleted'}), 200
    else:
        return jsonify({'status': 'not found'}), 404

if __name__ == '__main__':
    # Listen on all interfaces so Docker can route the traffic
    app.run(host='0.0.0.0', port=5001)
