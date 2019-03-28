import json
import string
import numpy as np

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
from math import ceil

LEVELS = ['lowerdiv', 'upperdiv', 'grad']

def cluster_courses(courses, num_clusters=5):
	"""
	courses is a dictionary with the format:
	courses[course_number] = {
			'course_number': course_number,
			'course_title': course_title,
			'number_of_units': unit_count,
			'description': description
		}

	vectorizer is a text vectorizer (either count or tfidf). 
	It has not yet been fit.
	"""

	# Clean the descriptions
	for num in courses:
		courses[num]['description'] = clean_description(courses[num]['description'])

	document_titles = []
	documents = []
	for num in courses:
		document_titles.append(num)
		documents.append(courses[num]['description'])

	vectorizer = TfidfVectorizer()
	X = vectorizer.fit_transform(documents)
	
	vectors = vectorizer.transform(documents).toarray()
	# print(len(documents))
	# print(vectors.shape)
	# print(vectors)
	# print(np.sum(vectors, axis=0))

	kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(vectors)
	cluster_labels = list(kmeans.labels_)

	clusters = {}
	i = 0
	for num in courses:
		clusters[num] = cluster_labels[i]
		i += 1

	# print(clusters)
	return clusters


def clean_description(text):
	for i in range(len(text)):
		if text[i] in string.punctuation:
			text = text[:i] + ' ' + text[i+1:]
	text = text.lower()
	return text


def parse_div(html_txt):
	s = str(html_txt)
	l = s.split('<li class="media category-list-item">')
	l = l[1:] # first blurb is not a course

	courses = {}

	for course in l:
		soup = BeautifulSoup(course, 'html.parser')
		course_title = str(soup.h3)[4:-5]
		course_number 	= course_title[:course_title.index('.')]
		course_name		= course_title[course_title.index('.')+2:]
		
		p = soup.find_all('p')
		unit_count = str(p[0])
		description = str(p[1])
		
		unit_count = unit_count[10:-4]
		description = description[3:-4]
		
		courses[course_number] = {
			'course_number': course_number,
			'course_title': course_title,
			'number_of_units': unit_count,
			'description': description
		}
	# print(courses)
	return courses

# def get_dict(major):
# 	d = {}
# 	for level in LEVELS:
# 		if level in data[major]:
# 			d[level] = parse_div(data[major][level])
# 	return d

def course_type(num):
	s = ''
	try:
		n = int(s.join(list(filter(str.isdigit, num))))
	except:
		return 'lowerdiv'
	if n < 100:
		return 'lowerdiv'
	if n < 200:
		return 'upperdiv'
	return 'grad'

def has_level(level, major):
		return level in data[major]

def get_split_data(major):
	# Combine the different levels together because the course data is mixed and not clean 
	courses = {}

	for level in LEVELS:
		if not has_level(level, major):
			continue
		d = parse_div(data[major][level])
		for c in d:
			if c in courses:
				continue
			courses[c] = d[c]

	# Split into actual levels
	course_data = {}
	for level in LEVELS:
		if not has_level(level, major):
			continue
		if level not in course_data:
			course_data[level] = {}
		for num in courses:
			if course_type(num) == level:
				course_data[level][num] = courses[num]

	return course_data


def load_json_to_dict(path):
	try:
		with open(path, 'r') as fp:
			return json.load(fp)
	except:
		print('PROBLEM WITH LOADING JSON DICT')

data = load_json_to_dict('descriptions.json')
majors = load_json_to_dict('major_list.json')['majors']

major_clusters = {}
for major in majors:
	major_clusters[major] = {}
	if major not in data:
		print('COULD NOT DO', major)
		continue
	course_data = get_split_data(major)

	for level in LEVELS:
		if not has_level(level, major):
			continue
		
		try:
			num_courses = len(course_data[level])
			num_clusters = ceil(num_courses / 3)

			clusters = cluster_courses(course_data[level], num_clusters)
			# print(clusters)
			cluster_lists = []
			for i in range(num_clusters):
				cluster_lists.append([])
			for c in clusters:
				cluster_lists[clusters[c]].append(c)
			
			major_clusters[major][level] = cluster_lists
		except:
			print('COULD NOT DO', major, level)


with open('clusters.json', 'w') as fp:
    json.dump(major_clusters, fp)

