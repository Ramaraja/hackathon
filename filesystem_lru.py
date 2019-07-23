# to find lease recently used files and size
from __future__ import print_function 
import os
import time
import heapq
import matplotlib.pylab as plt
import numpy as np
import math


# to get top 10 file/application which opened least recent 
def get_top_lru(fs, top=10):
	# top = []
	print("getting files")
	files = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(fs):
		# print f
		for file in f:
			# if '.json' in file:
			files.append(os.path.join(r, file))

	# for f in files:
	# 	print(time.ctime(os.path.getatime(f)))
	# lrc_files = files
	lrc_files = heapq.nsmallest(
			int(top), files, key=os.path.getatime)

	print (lrc_files)

	big_files = heapq.nlargest(
				int(top), lrc_files, key=os.path.getsize)
	# top_files_dict = {}
	top_files = []

	for file in big_files:
		print(time.ctime(os.path.getatime(file)))

		# top_files_dict.update({file: os.path.getsize(file)})
		top_files.append({"file":file,"size": os.path.getsize(file)})
	sorted(top_files, key = lambda i: i['size'])
	print(top_files)
	plots = []
	plots.append([f['file'] for f in top_files])
	plots.append([f['size'] for f in top_files])

	return top_files

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

# cwd = os.getcwd()
# l = get_top_lru("00b392fd-c977-4be5-bf20-54c43a3a2a13")

# l = get_top_lru("/Users/rramacha/GenOps/")
# plot(l)


