
from flask import Flask, send_file

# app
app = Flask(__name__)
@app.route('/', methods = ['GET'])
def index_get():
    return send_file("./index.html")
@app.route('/frame_compass.html', methods = ['GET'])
def compass_get():
    return send_file("./frame_compass.html")
@app.route('/frame_graph_distances.html', methods = ['GET'])
def distances_get():
    return send_file("./frame_graph_distances.html")
@app.route('/frame_heatmap.html', methods = ['GET'])
def heatmap_get():
    return send_file("./frame_heatmap.html")
@app.route('/frame_map.html', methods = ['GET'])
def map_get():
    return send_file("./frame_map.html")
@app.route('/frame_recent_data.html', methods = ['GET'])
def recent_get():
    return send_file("./frame_recent_data.html")
# main
if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=8000, threaded=True)
