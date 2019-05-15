from major_graph import MajorGraph
import json

print_errors = False

major_reqs = json.loads(open("cs_reqs.json").read())
acronym_mapping = json.loads(open("acronym_mapping.json").read())
prerequisites = json.loads(open("prereqs.json").read())
for major in prerequisites:
    if major not in acronym_mapping:
        if print_errors:
            print(major + " Not Found")
        continue
    acro_major = acronym_mapping[major]
    prerequisites[acro_major] = prerequisites[major]
    prerequisites.pop(major, None)
    major_classes = prerequisites[acro_major]
    for class_name in major_classes:
        collections = major_classes[class_name]
        for collection in collections:
            for cl in collection:
                spl = cl.rsplit(' ', 1)
                if spl[0] not in acronym_mapping:
                    if print_errors:
                        print(spl[0] + " Not Found")
                    continue
                dept = acronym_mapping[spl[0]]
                num = spl[1]
                cl = dept + " " + num


major = MajorGraph()

for req in major_reqs:
    for subreq in major_reqs[req]:
        for categories in major_reqs[req][subreq]:
            if categories == "NEEDS":
                continue
            for c in major_reqs[req][subreq][categories]:
                dept = c['DEPT'].strip(" *")
                num = c['NUM'].strip(" *")
                dept += " "
                class_name = ""
                class_name += dept
                class_name += num
                major.add_vertex(class_name)

for cl in major.m_vertices:
    spl = cl.rsplit(' ', 1)
    dept = spl[0]
    num = spl[1]
    if dept not in prerequisites:
        if print_errors:
            print(dept + " not found in prerequisites") 
        continue
    prs = prerequisites[dept]
    if cl not in prs:
        if print_errors:
            print(cl + " not found in " + dept)
        continue
    class_prereqs = prs[cl]
    # this part is fucking bullshit
    for obj in class_prereqs:
        for c in obj:
            spl2 = c.rsplit(' ', 1)
            if spl2[0] not in acronym_mapping:
                if print_errors:
                    print(spl2[0] + " Not Found blabla")
                continue
            dept = acronym_mapping[spl2[0]]
            num = spl2[1]
            c = dept + " " + num
            major.add_edge(c, cl)

##########################

CLASS_NAME = "COM SCI 180"
print(CLASS_NAME + " unlocks:")
major.print_unlocks(CLASS_NAME)

# print("========")
# major.print_edges()
    
