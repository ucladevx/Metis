import sys
import os
import re

#Parse HTML and pull courses into a string
def stringifyCourses(string):
	coursePattern = r'class="popover-right".*javascript\:void\(0\)\"\>(.*?)\<\/a\>'
	courses = re.findall(coursePattern,string)
	courses = swapAndInCourse(courses)
	
	coursesString = ' '.join(courses)
	coursesString = re.sub( r"\s+" , " " ,coursesString)

	return coursesString

############################################################################################################

#Go through list of courses and swap 'and' with '&' to avoid double 'and' conflicts later
def swapAndInCourse(courses):
	#print(courses)
	for index in range(len(courses)):
		courses[index] = re.sub('and','&',courses[index]).strip()
		if courses[index][-1]=='&':
			courses[index] = courses[index][:-1] +'and'

	return courses 
'''
def swapAndInCourse(courses):
	patterns = [r'and',r'or$',r'\)']
	#print(courses)
	for index in range(len(courses)):
		flag = -1
		for pattern in patterns:
			flag += len(re.findall(pattern,courses[index]))
		if flag > 0:
			courses[index] = re.sub('and','&',courses[index], 1)
		if courses[index][-1]=='&':
			courses[index] = courses[index][:-1] +'and'
	print(courses)
	return courses 
'''

#Turn '&' symbols back into 'and' after parsing and creating dependencies
def unswapAndInCourse(courses):
	for index in range(len(courses)):
		if type(courses[index]) is str:
			courses[index] = re.sub('^& ','',courses[index])
			courses[index] = re.sub('&','and',courses[index])
		else:
			unswapAndInCourse(courses[index])
	return

def parseString(string, courses, recursed):
	#Check for double parentheses
	#print(string)
	check = re.search(r'\((\(.*\))\)',string)

	if check:
		string = re.sub(r'\(\((.*)\)\)','',string)

		courses.append(parseString(check.group(1),[],True))
	
		
	#Identify all the different strings of 'or's, always contained in parentheses unless entire string consists of 1 'or' string
	parentheses = re.findall(r'\((.*?)\)',string)
	#print(parentheses)
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
	string = re.sub(r'\(.*?\)+', '___', string)
	
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
#fix this for loop
	#Look at each string identified inside a parenthesis
	for group in parentheses:
		inner = re.findall(r'(.*?) or',group)
		lastOr = re.search(r'.* or (.*?)$',group)

		if lastOr:
			#Check if there was an internal parenthesis grouping
			innerParentheses = re.search(r'\((.*?)\)',group)
			if innerParentheses:
				inner.append(parseString(innerParentheses.group(1),[],True))
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
		#Strip and then append list of the "or" courses to the main course requisite list
			for index in range(len(inner)):
				inner[index]=inner[index].strip()
			inner.append("Or")
		courses.append(inner)

	if not re.search('and',string) and len(parentheses)!=0:
		courses=[courses]

	unswapAndInCourse(courses)

	index = 0
	while index < len(courses):
		if courses[index]=='':
			courses.pop(index)
		else:
			index+=1

	if recursed and len(courses)>1:
		courses.append("And")

	return courses

############################################################################################################

def parseDependencyTypes(dependencies,html,mapping):
	for index in range(len(dependencies)):
		if type(dependencies[index]) is str:
			course = dependencies[index]
			if course =='And' or course =='Or':
				continue
			pattern = course + r'[\S\s]*?data-content=\"(.*?)\:'

			mapping[course] = re.search(pattern,html,re.DOTALL).group(1)
		else:
			parseDependencyTypes(dependencies[index],html,mapping)
	return

############################################################################################################

def processOrBlock(layer,pathways):

	orPathways = []
	for sublayer in layer:
		if type(sublayer) is str:
			if sublayer=='Or':
				continue
			orPathways.append([sublayer])
		else:
			subPathway = []
			for course in sublayer[:-1]:
				subPathway.append(course)
			orPathways.append(subPathway)
	returnedPathways = []
	for index in range(len(orPathways)):
		for pathway in pathways:
			returnedPathways.append(pathway + orPathways[index])
	
	return returnedPathways	

def createPathways(dependencies,pathways):
	#root and layer2 are 'and' (required)
	root = []
	layer2 = []

	#each element in first layer of dependencies is parsed in an 'and' structure
	for layer1group in dependencies:
		if type(layer1group) is str:
			root.append(layer1group)
		else:
			layer2.append(layer1group)

	#If no complicated layers, there's just 1 pathway
	pathways.append(root)

	if len(layer2)==0:
		return pathways

	#peel second layer if no courses in root, and 1 list in layer2
	if len(layer2)==1 and len(root)!=0:
		layer2=layer2[0]
	


	if len(layer2)==1:
		#Peel outer, useless layer if by itself
		#layer 3 and onwards are parsed in an 'or' structure, unless explictly stated as 'And' and the end of a list
		layer3 = layer2[0]

		#Not sure if orStatus can be False, may need to handle if that case comes up
		orStatus = True
		if type(layer3[-1]) is str and layer3[-1] == 'And':
			orStatus = False

		#Appends the different 'or' paths to each subpath in pathways
		if orStatus:
			pathways = processOrBlock(layer3,pathways)
			
	else:
	#Parses each sublayer in layer2
		#check if every 'sublayer' element is string
		allString = False
		for index in range(len(layer2)):
			if type(layer2[index]) is str:
				if index == (len(layer2) - 1):
					allString = True
			else:
				break
				
		if allString:
			pathways = processOrBlock(layer2,pathways)
		else:
		#doLater allows for most-complete pathway to be complete before parsing sublists, holds these sublists for later
			doLater = []
			for sublayer in layer2:
				#print(sublayer)
				tempPathways = []

				#If [...]'s first element is a string
				if type(sublayer[0]) is str:
					#If the last element in [...] is 'Or' or a list, either of which denotes an 'or' list
					if (type(sublayer[-1]) is str and sublayer[-1] == 'Or') or type(sublayer[-1]) is not str:
						for course in sublayer:
							if type(course) is str and course=='Or':
								continue
							#Because this is an 'or' path, append this course in the sublayer to the content's of main path
							#Stored temporarily in tempPathways to not mess up the main branch
							for pathway in pathways:
								tempPathways.append(pathway + [course])
				#Else there's a sublist inside
				else:
					if len(sublayer)==1:
						sublayer = sublayer[0]
					doLater.append(sublayer)

				if len(pathways) < len(tempPathways):
					pathways = tempPathways
			
			for sublayer in doLater:
				pathways = processOrBlock(sublayer,pathways)

	#get rid of internal blocks if exist
	finalPathways = []
	for pathway in pathways:
		current = []
		for course in pathway:
			if type(course) is str:
				current.append(course)
			else:
				for subcourse in course:
					if subcourse != 'And':
						current.append(subcourse)
		finalPathways.append(current)

	print('')
	return finalPathways

############################################################################################################

def main():
	examples = ['example9.txt']
	for example in examples:
		with open(example, 'r') as myfile:
			pageSource = myfile.read()

		#Get course title from html
		courseTitle=re.search(r'subject_class[\s\S]*?( .*?)</p></div>',pageSource).group(1).strip()
		courseTitle = " ".join(courseTitle.split())
		print(courseTitle)

		stringOfCourses = stringifyCourses(pageSource)

		dependencies = parseString(stringOfCourses,[],False)
		print( dependencies)
		print('')
		courseDependencyTypes = dict()
		
		parseDependencyTypes(dependencies,pageSource,courseDependencyTypes)
		#print(courseDependencyTypes)
		pathways = createPathways(dependencies,[])
		print(pathways)
if __name__ == '__main__':
	main()