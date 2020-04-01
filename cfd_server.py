import os
import json
import numpy as np
from bottle import Bottle, run

# parameters for loading of files
# will be replaced when call to database available
file_dir = "data/CFD_result"
files = os.listdir(file_dir)
count = 0

# load indices of CFD data that are inside the lab
indices_filename = 'indices_inside_lab.json'
n_point = 2500
with open(indices_filename, 'r') as f:
    indices = json.load(f)

def get_latest_cfd_data():
	global count

	filename = files[count % len(files)]
	with open(os.path.join(file_dir, filename), 'r') as f:
		f.readline()
		lines = f.readlines()
	count += 5
	return lines

def filter_inside_reduce(data, n_points):
	np.random.seed(23)
	select_indices = np.random.choice(indices, n_points, replace=False)
	data = np.array(data)
	select_data = data[select_indices]
	return select_data

def data_to_text(data):
	text = ''
	for line in data:
		text += line
	return text


app = Bottle()
 
@app.route('/hello')
def hello():
	print("received hello")
	return "Hello World!"

@app.route('/get_cfd')
def get_cfd():
	data = get_latest_cfd_data()
	data_processed = filter_inside_reduce(data, n_points=2500)
	print(data_processed.shape)
	return data_to_text(data_processed)

run(app, host='0.0.0.0', port=8080)