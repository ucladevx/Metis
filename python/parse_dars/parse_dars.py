from bs4 import BeautifulSoup
import re
import json

soup = BeautifulSoup(open(".\\econ_dars.html"), "html.parser")

requirementStatus_ = re.compile('requirement Status_.*?rtabx_\d*')
reqs = soup.find_all('div', attrs={'class': requirementStatus_})

major_reqs = {}

# remove br


for req in reqs:

    # get req title!
    titles = req.find_all('div', attrs={'class': 'reqTitle'})
    title = "".join(str(x) for x in titles[0]) # preserves more information
    #title = "".join(str(x) for x in titles[0].contents[0])
    #title = ' '.join(title.split())
    
    major_reqs[str(title)] = {}
    major_reqs[str(title)]['CLASSES'] = []
    major_reqs[str(title)]['SUBREQUIREMENTS'] = []
        
    # parse SELECT FROM:
    classes = req.find_all('span', attrs={'class': 'course draggable'})

    for c in classes:
        # print(c['department'], c['number'])
        cl = [c['department'], c['number']]
        major_reqs[str(title)]['CLASSES'].append(cl)
    
    # parse ELECTIVE stuff
    subreqBodies = []
    sections = req.find_all('div', attrs={'class': 'subreqBody'})
    for s in sections:
        subreqBody = {}
        reqTitle = s.find('span', attrs={'class': 'subreqTitle'})
        if len(reqTitle.contents) == 0:
            continue
        reqTitle = reqTitle.contents[0]
        subreqBody['TITLE'] = title
        subreqBody['NOT_FROM'] = []
        notFrom = s.find_all('tr', attrs={'class': 'notfromcourses'})
        for nf in notFrom:
            classes = nf.find_all('span', attrs={'class': 'course'})
            for c in classes:
                cl = [c['department'], c['number']]
                subreqBody['NOT_FROM'].append(cl)
        subreqBodies.append(subreqBody)
    major_reqs[str(title)]['SUBREQUIREMENTS'] = subreqBodies
    print(subreqBodies)

        

    # completedClasses = req.find_all('td', attrs={'class': 'course', 'aria-label': 'course'})
    # for c in completedClasses:
    #     info = c.string[::-1] # reverse string
    #     arr = info.split(' ', 1)
    #     arr.reverse()
    #     for i in range(len(arr)):
    #         arr[i] = arr[i][::-1]
    #     print(" ".join(arr))
    #     major_reqs[str(title)].append(arr)

# print(major_reqs)
with open('econ_reqs.json', 'w') as fp:
    json.dump(major_reqs, fp)