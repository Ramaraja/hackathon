# to find lease recently used files and size
from __future__ import print_function 
import os
import time
import heapq
import matplotlib.pylab as plt
import numpy as np
import math
import re
import datetime
import json


# to get top 10 file/application which opened least recent 
def get_top_lru(fs, top=100, days=None):
	# top = []
	files = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(fs):
		for file in f:
			# if '.json' in file:
			files.append(os.path.join(r, file))

	lru_files = heapq.nsmallest(
			int(top), files, key=os.path.getatime)

	big_files = heapq.nlargest(
				int(top), lru_files, key=os.path.getsize)

	app_info = get_application_info(big_files, days)
	data = get_aggregated_data(app_info, files)
	return data

def get_application_info(files_list, days):
	app_ids = []
	for file in files_list:
		m = re.search('workspace/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', file)
		if m:
			app_id = m.group(1)
			# return app_id
			if days:
				ct = datetime.datetime.fromtimestamp(time.time())
				at = datetime.datetime.fromtimestamp(os.path.getatime(file))
				delta = ct - at
				if delta.days >= int(days):
					app_ids.append(app_id)
			else:
				app_ids.append(app_id)
		else:
			print ("No matching application. This can be a common file. skip for now!!")
			# return False
	# remove duplicates
	app_ids = list(set(app_ids))
	return app_ids

def get_aggregated_size(files):
	size = 0
	if type(files) == list:
		for file in files:
			size = size + int(os.path.getsize(file))
		return size
	elif type(files) == str:
		return int(os.path.getsize(files))

def get_aggregated_data(app_info, files):
	final_data = []
	app_files=[]
	for app in app_info:
		for f in files:
			if app in f:
				app_files.append(f)
		# app_files = [f for f in files if app in f]
		size = get_aggregated_size(app_files)
		app_name = get_app_name(app, files)
		final_data.append({"application": app, "size": size, "name": app_name})
		# not considering common files now. may be later
		# else:
		# 	size = get_aggregated_size(item)
		# 	final_data.append({"application": "common", "size": size, "file": item})

	return final_data

def get_app_name(app, files):
	for f in files:
		if app in f and f.split('/')[-1] == 'manifest.json':
			try:
				with open(f) as json_file:
					data = json.load(json_file)
				return data['name']
			except:
				return "Unknown app"

def validate_timestamp(app_files):
	pass

def filter_by_days(day, app_files):
	pass

def plot(data):
	x, y = data
	# plt.plot(x, y)
	# plt.show()

	index = np.arange(len(x))
	plt.bar(index, y)
	plt.xlabel('File', fontsize=5)
	plt.ylabel('Size', fontsize=5)
	plt.xticks(index, x, fontsize=5, rotation=30)
	plt.title('LRU files and size')
	plt.show()

def convert_size(size_bytes): 
	if size_bytes == 0: 
		return "0B" 
	size_name = ("B", "KB", "MB", "GB") 
	i = int(math.floor(math.log(size_bytes, 1024)))
	power = math.pow(1024, i) 
	size = round(size_bytes / power, 2) 
	return "%s %s" % (size, size_name[i])


# l = get_top_lru("../00b392fd-c977-4be5-bf20-54c43a3a2a13", days=1)


