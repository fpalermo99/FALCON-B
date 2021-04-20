
from flask import Flask, send_file
from subprocess import Popen, PIPE

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
@app.route('/datagetter', methods = ['GET'])
def data_get():
    f = 'data_log.txt'
    # Get the last line from the file
    p = Popen(['tail','-1',f],shell=False, stderr=PIPE, stdout=PIPE)
    res,err = p.communicate()
    if err:
        print(err.decode())
        return {"dist":0, "brng":0, "zone":1.1}
    else:
        # Use split to get the part of the line that you require
        res = res.decode().split(',')
        dst = res[0].split(' ')[1]
        brng = res[1].split(' ')[1]
        zone = res[2].split(' ')[1]
        return {"dist":int(dst), "brng":int(brng), "zone":float(zone)}
# main
if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=8000, threaded=True)
