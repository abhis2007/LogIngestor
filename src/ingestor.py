from flask import Flask, request, g, jsonify, render_template
import sqlite3
from datetime import datetime, timezone
from flask_socketio import SocketIO
from flask_caching import Cache

app = Flask(__name__, template_folder="../templates")
# app.debug = True
socketio = SocketIO(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 360})

STR_AND = " AND "
ITEMS_PER_PAGE = 15
CACHED_DATA = "cached_data"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('loggerDb.db')
    return db

# Function to get the SQLite cursor
def get_cursor():
    return get_db().cursor()

# Create the logs table if it doesn't exist
with app.app_context():
    dbHandler = get_cursor()
    dbHandler.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            level TEXT,
            message TEXT,
            resourceId TEXT,
            timestamp TIMESTAMP,
            traceId TEXT,
            spanId TEXT,
            "commit" TEXT,
            parentResourceId TEXT
        )
    ''')
    dbHandler.execute('''CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level)''')

    dbHandler.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS logs_fts
        USING FTS4(message)
    ''')    
    
    dbHandler.execute('''CREATE INDEX IF NOT EXISTS idx_timestamp ON logs(timestamp)''')    
    dbHandler.execute('''CREATE INDEX IF NOT EXISTS idx_logs_resourceId ON logs(resourceId)''')
    dbHandler.execute('''CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp)''')
    dbHandler.execute('''CREATE INDEX IF NOT EXISTS idx_logs_traceId ON logs(traceId)''')    
    dbHandler.execute('''CREATE INDEX IF NOT EXISTS idx_logs_spanId ON logs(spanId)''')   
    dbHandler.execute('''CREATE INDEX IF NOT EXISTS idx_logs_commit ON logs("commit")''') 
    dbHandler.execute('''CREATE INDEX IF NOT EXISTS idx_logs_parentResourceId ON logs("parentResourceId")''')

    get_db().commit()

# Close the SQLite connection after each request
@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def index():
    try:
        with app.app_context():
            dbHandler = get_cursor()
            dbHandler.execute('SELECT * FROM logs')
            result = dbHandler.fetchall()
        cache.set(CACHED_DATA, result)
        return render_template("home.html", results = result[:4*ITEMS_PER_PAGE][:4*ITEMS_PER_PAGE])
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/load-more/<int:page>', methods=['GET'])
def load_more(page):
    start = page * ITEMS_PER_PAGE
    end = (page + 1) * ITEMS_PER_PAGE
    currentPageData = cache.get(CACHED_DATA)
    return currentPageData[start:end]

@app.route('/ingest', methods=['POST'])
def ingest_logs():
    try:
        json_data = request.get_json()
        level = json_data.get("level")
        message = json_data.get("message")
        resourceId = json_data.get("resourceId")
        timestamp = json_data.get("timestamp")

        timestamp_datetime = datetime.fromisoformat(timestamp)
        timestamp_utc = timestamp_datetime.replace(tzinfo=timezone.utc)
        timestamp_isoformat = timestamp_utc.isoformat()

        traceId = json_data.get("traceId")
        spanId = json_data.get("spanId")
        commit = json_data.get("commit")
        parentResourceId = json_data.get("metadata", {}).get("parentResourceId")
        
        with app.app_context():
            dbHandler = get_cursor()
            dbHandler.execute('''
                INSERT INTO logs (level, message, resourceId, timestamp, traceId, spanId, "commit", parentResourceId)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (level, message, resourceId, timestamp_isoformat, traceId, spanId, commit, parentResourceId))
            get_db().commit()

            dbHandler.execute('''
                INSERT INTO logs_fts (message)
                VALUES (?)
            ''', (message, ))
            
            get_db().commit()
        return "Log entry ingested successfully."
    except Exception as e:
        return f"Error ingesting log entry: {str(e)}"

@app.route('/search/message/', methods=['POST'])
def searchByMessage():
    try:
        resId = request.form.get("srchVal")
        with app.app_context():
            dbHandler = get_cursor()
            query = """
                SELECT logs.*
                FROM logs
                JOIN logs_fts ON logs.rowid = logs_fts.rowid
                WHERE logs_fts.message MATCH ?;
            """
            dbHandler.execute(query, (resId,))
            result = dbHandler.fetchall()
            cache.set(CACHED_DATA, result)
        return render_template("home.html", results = result[:4*ITEMS_PER_PAGE])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search/timestamp/', methods=['POST'])
def searchByTimeStamp():
    dbHandler = get_cursor()
    try:
        utcDateTimeFrom = request.form.get("utcDateTimeFrom")
        original_datetimeFrom = datetime.strptime(utcDateTimeFrom, "%Y-%m-%dT%H:%M")
        fromDate = original_datetimeFrom.replace(tzinfo=timezone.utc).isoformat()

        utcDateTimeTo = request.form.get("utcDateTimeTo")
        queryStr = "SELECT * FROM logs WHERE timestamp"
        if utcDateTimeTo == "":
            queryStr = queryStr + "='" + fromDate + "';" 
        else:
            original_datetimeTo = datetime.strptime(utcDateTimeTo, "%Y-%m-%dT%H:%M")
            toDate = original_datetimeTo.replace(tzinfo=timezone.utc).isoformat()
            queryStr = queryStr + " BETWEEN " + "'" + fromDate + "' AND " + "'" + toDate + "'"
           
        dbHandler.execute(queryStr)
        result = dbHandler.fetchall()  
        cache.set(CACHED_DATA, result)
        return render_template("home.html", results = result[:4*ITEMS_PER_PAGE] )
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/search/resourceId/', methods=['POST'])
def search_by_resource_id():
    try:
        resId = request.form.get("srchVal")
        with app.app_context():
            dbHandler = get_cursor()
            dbHandler.execute('SELECT * FROM logs WHERE resourceId = ?', (resId,))
            result = dbHandler.fetchall()        
        cache.set(CACHED_DATA, result)

        return render_template("home.html", result = result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_logs_by_level(level):
    with app.app_context():
        dbHandler = get_cursor()
        dbHandler.execute(''' SELECT * FROM logs WHERE level = ? ''', (level,))
        result = dbHandler.fetchall()
    cache.set(CACHED_DATA, result)
    return result
   
@app.route('/search/level/', methods=['POST'])
def searchByLevel():
    try:
        level = request.form.get("srchVal")
        result = get_logs_by_level(level)
        result = cache.get(level)

        if result is None :
            result = get_logs_by_level(level)
            cache.set(level, result)
        
        return render_template("home.html", results = result[:4*ITEMS_PER_PAGE])

    except Exception as e:
        return f"Error searching by level: {str(e)}"
    
@app.route('/search/spanId/', methods=['POST'])
def search_by_span_id():
    try:
        resId = request.form.get("srchVal")
        with app.app_context():
            dbHandler = get_cursor()
            dbHandler.execute('SELECT * FROM logs WHERE spanId = ?', (resId,))
            result = dbHandler.fetchall()
        cache.set(CACHED_DATA, result)
        return render_template("home.html", results = result[:4*ITEMS_PER_PAGE])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search/commitId/', methods=['POST'])
def search_by_commit_id():
    try:
        resId = request.form.get("srchVal")
        with app.app_context():
            dbHandler = get_cursor()
            dbHandler.execute('SELECT * FROM logs WHERE "commit" = ?', (resId,))
            result = dbHandler.fetchall()
        cache.set(CACHED_DATA, result)
        return render_template("home.html", results = result[:4*ITEMS_PER_PAGE])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/search/parentResourceId/', methods=['POST'])
def search_by_parRes_id():
    try:
        resId = request.form.get("srchVal")
        with app.app_context():
            dbHandler = get_cursor()
            dbHandler.execute('SELECT * FROM logs WHERE parentResourceId = ?', (resId,))
            result = dbHandler.fetchall()
        cache.set(CACHED_DATA, result)
        return render_template("home.html", results = result[:4*ITEMS_PER_PAGE])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def formQuery(columnName, filterValue):
    query = columnName + " = '" + filterValue + "'"
    return query

@app.route('/refine_search/', methods=['POST'])
def advanceSearch():
    level = request.form.get('level_AS')
    message = request.form.get('message_AS')
    res = request.form.get('resourceId_AS')
    traceId = request.form.get('traceId_AS')
    spanId = request.form.get('spanId_AS')
    commit = request.form.get('commit_AS')
    parResId = request.form.get('parentResourceId_AS')
    filterQuery = "SELECT * FROM logs WHERE " ; 
    
    count = 0
    if level :
        filterQuery += formQuery("level", level)
        count += 1
    
    if message :
        if count :
            filterQuery += STR_AND 
        filterQuery += formQuery("message", message)
        count += 1

    if res:
        if count:
            filterQuery += STR_AND
        filterQuery += formQuery("resourceId", res)
        count += 1
    if traceId:
        if count:
            filterQuery += STR_AND
        filterQuery += formQuery("traceId", traceId)
        count += 1

    if spanId:
        if count:
            filterQuery += STR_AND
        filterQuery += formQuery("spanId", spanId)
        count += 1

    if commit:
        if count:
            filterQuery += STR_AND
        filterQuery += formQuery("\"commit\"", commit)
        count += 1

    if parResId:
        if count:
            filterQuery += STR_AND
        filterQuery += formQuery("parentResourceId",parResId )
        count += 1

    utcDateTimeFrom = request.form.get("utcDateTimeFrom")
    if utcDateTimeFrom:
        original_datetimeFrom = datetime.strptime(utcDateTimeFrom, "%Y-%m-%dT%H:%M")
        fromDate = original_datetimeFrom.replace(tzinfo=timezone.utc).isoformat()
        utcDateTimeTo = request.form.get("utcDateTimeTo")
        if utcDateTimeTo == "":
            if count:
                filterQuery += STR_AND
            filterQuery += "timestamp='" + fromDate + "';" 
        else:
            if count:
                filterQuery += STR_AND
            original_datetimeTo = datetime.strptime(utcDateTimeTo, "%Y-%m-%dT%H:%M")
            toDate = original_datetimeTo.replace(tzinfo=timezone.utc).isoformat()
            filterQuery += "timestamp" + " BETWEEN " + "'" + fromDate + "' AND " + "'" + toDate + "'"
           
    try:
        with app.app_context():
            dbHandler = get_cursor()
            dbHandler.execute(filterQuery)
            result = dbHandler.fetchall()
        cache.set(CACHED_DATA, result)
        return render_template("home.html", results = result[:4*ITEMS_PER_PAGE])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/search/traceId/', methods=['POST'])
def search_by_trace_id():
    try:
        resId = request.form.get("srchVal")
        with app.app_context():
            dbHandler = get_cursor()
            dbHandler.execute('SELECT * FROM logs WHERE traceId = ?', (resId,))
            result = dbHandler.fetchall()
        cache.set(CACHED_DATA, result)
        return render_template("home.html", results = result[:4*ITEMS_PER_PAGE])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
if __name__ == '__main__':
    socketio.run(app, port=3000)
    # app.run(port=3000)