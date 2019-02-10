import sys
import os
import re

#Go through list of courses and swap 'and' with '&' to avoid double 'and' conflicts later
def swapAndInCourse(courses):
	patterns = [r'and',r'or$',r'\)']
	#print(courses)
	for index in range(len(courses)):
		flag = -1
		for pattern in patterns:
			flag += len(re.findall(pattern,courses[index]))
		if flag > 0:
			courses[index] = re.sub('and','&',courses[index], 1)
	
	return courses 

#Turn '&' symbols back into 'and' after parsing and creating dependencies
def unswapAndInCourse(courses):
	for index in range(len(courses)):
		if type(courses[index]) is str:
			courses[index] = re.sub('^& ','',courses[index])
			courses[index] = re.sub('&','and',courses[index])
		else:
			unswapAndInCourse(courses[index])
	return

#Parse HTML and pull courses into a string
def stringifyCourses(string):
	coursePattern = r'class="popover-right".*javascript\:void\(0\)\"\>(.*?)\<\/a\>'
	courses = re.findall(coursePattern,string)
	courses = swapAndInCourse(courses)
	
	coursesString = ' '.join(courses)
	coursesString = re.sub( r"\s+" , " " ,coursesString)
	#print(coursesString)
	#print(re.search(r'\((.*)\)',coursesString).group(1))
	#coursesString = re.search(r'\((.*)\)',coursesString).group(1)
	#print(coursesString)
	return coursesString

def parseString(string, courses):
	#Check for double parentheses
	#print(string)
	check = re.search(r'\((\(.*\))\)',string)

	if check:
		string = re.sub(r'\((.*)\)','',string)
		courses.append(parseString(check.group(1),[]))
	
	#Identify all the different strings of 'or's, always contained in parentheses unless entire string consists of 1 'or' string
	parentheses = re.findall(r'\((.*?)\)',string)
	for index in range(len(parentheses)):
		left = 0
		right = 0
		for ch in parentheses[index]:
			if ch=='(':
				left+=1
			if ch==')':
				right+=1
		for _ in range(left-right):
			parentheses[index] = parentheses[index] + ')'



	#Replace these parentheses with a ___
	string = re.sub(r'\(.*?\)', '___', string)

	#Identify the requisie courses before an 'and'
	ands = re.findall(r'([^_]*?) and', string)
	#Identify the last requisite course that follows an 'and'
	lastAnd = re.search(r'.* and ([^_]*?)$',string)
	if lastAnd:
		ands.append(lastAnd.group(1))
	for group in ands:
		if len(group)==0:
			continue
		courses.append(group.strip())

	#Look at each string identified inside a parenthesis
	for group in parentheses:
		inner = re.findall(r'(.*?) or',group)
		lastOr = re.search(r'.* or (.*?)$',group)

		if lastOr:
			#Check if there was an internal parenthesis grouping
			innerParentheses = re.search(r'\((.*?)\)',group)
			if innerParentheses:
				inner.append(parseString(innerParentheses.group(1),[]))
			else:
				inner.append(lastOr.group(1))

		#If there's nothing from checking for "or"s, try "and"
		if len(inner)==0:
			inner = re.findall(r'(.*?) and',group)
			lastAnd = re.search(r'.* and (.*?)$',group)
			if lastAnd:
				inner.append(lastAnd.group(1))
			inner.append("And")
		else:
			inner.append("Or")

		for index in range(len(inner)):
			if type(inner[index]) is str:
				inner[index]=inner[index].strip()

		courses.append(inner)

	#Handle if the whole string is a big string of 'or's, or if there's just a single requisite
	if len(courses) == 0:

		#Find all the ors except the last one
		inner = re.findall(r'(.*?) or',string)

		#Find the last or
		lastOr = re.search(r'.* or (.*?)$',string)
		if lastOr:
			inner.append(lastOr.group(1))

		#If there were no "or" in the string, there was just a single requisite
		if len(inner)==0:
			inner = string.strip()
		else:
		#Sanitize and then append list of the "or" courses to the main course requisite list
			for index in range(len(inner)):
				inner[index]=inner[index].strip()
			inner.append("Or")
		courses.append(inner)
	
	unswapAndInCourse(courses)

	for index in range(len(courses)):
		if courses[index]=='':
			courses.pop(index)

	return courses
	

def main():
	examples = ['example2.txt']
	for example in examples:
		with open(example, 'r') as myfile:
			string = myfile.read()
		stringified = stringifyCourses(string)
		print(parseString(stringified,[]))

if __name__ == '__main__':
	main()