from bs4 import BeautifulSoup

class CCLEHTMLParser:
	def __init__(self):
		pass

	def _remove_tags(self, l):
		"""
		Takes a list of html strings and returns only the text outside all '<' and '>' parentheses
		Arguments:
		l -- A list of strings containing html tags
		"""
		lclean = []
		for s in l:
			st = []
			clean_s = ' '
			tags = []

			# Retrieve start and end indices of all tags
			for i in range(len(s)):
				c = s[i]
				if c == '<':
					st.append(i)
				if c == '>':
					tstart = st.pop()
					tags.append((tstart, i))

			# Retrieve text outside tags
			for i in range(len(s)):
				in_tag = False
				for tag in tags:
					if tag[0] <= i and i <= tag[1]:
						in_tag = True
						break
				if in_tag:
					continue
				clean_s = clean_s + s[i]

			lclean.append(clean_s.strip())

		return lclean

	def get_class_professor_list(self, html_text):
		"""
		Takes the html source for a page and returns the list of classes, professors
		"""
		html_doc = html_text

		soup = BeautifulSoup(html_doc, 'html5lib')

		rows = str(soup.body.table.tbody).split('<tr class="">')[1:]
		classes = []

		for r in rows:
			class_info = self._remove_tags(r.split('</td>\n')[1:])
			classes.append(class_info)

		n = len(classes)
		classes.append(classes[n - 1][4:])
		for i in range(n + 1):
			classes[i] = classes[i][:3]

		return classes


# html_text = open('comsci.html').read()
# parser = CCLEHTMLParser()
# cs_classes = parser.get_class_professor_list(html_text)

# for c in cs_classes:
# 	print(c)
