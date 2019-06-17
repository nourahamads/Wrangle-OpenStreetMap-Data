
# coding: utf-8

# ###### code of parsing data file :

# In[5]:

import xml.etree.ElementTree as ET
import re
from collections import defaultdict
import pprint
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET


import cerberus
import schema

tree = ET.parse('C:\Users\hp\Desktop\las-vegas_nevada.osm')
root = tree.getroot() 


# ###### audit the street type ( code to find error)

# In[6]:

#!/usr/bin/env python

# this is code from udacity website 

osm_file = open("C:\Users\hp\Desktop\las-vegas_nevada.osm", "r")

street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 

def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)    

if __name__ == '__main__':
    audit()


# ###### code of audit the stree type 

# In[7]:

##this is code from udacity website 

LASOSMFILE = open("C:\Users\hp\Desktop\las-vegas_nevada.osm", "r")
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types= defaultdict(set)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
           "S":"Street",
           "pkwy":"Parkway",
            "Rd":"Road",
            "RD": "Road",
            "Rd.":"Road",
            "Rds":"Road",
             "Parkway":"parkway",
             "Dr": "Drive",
             "Dr.":"Drive",
              "drive":"Drive",
              "B":"Boulevard",
              "blvd":"Boulevard",
               "Blvd":"Boulevard",
               "Blvd.":"Boulevard",
               "Bonneville":"Boulevard",
               "AVE":"Avenue",
                "Ave":"Avenue",
                 "ave":"Avenue",
                 "Ave.":"Avenue"
            
            }




def audit_street_type(street_types,street_name):
    m=street_type_re.search(street_name)
    if m :
        street_type=m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)



def is_street_name(elem):
    return (elem.attrib['k']=="addr:street")

def audit():
    for event, elem in ET.iterparse(LASOSMFILE, events=("start",)):
        if elem.tag =="way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    #pprint.pprint(dict(street_types))
    return street_types    
    
    

def update_name(name, mapping):

    m = street_type_re.search(name)
    if m.group() in mapping.keys():
            name = re.sub(m.group(), mapping[m.group()], name)
                
    return name

st_types = audit()
pprint.pprint(dict(st_types))

for st_type, ways in st_types.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        print name, "===>", better_name


audit()


# #### audit postal code . 

# In[10]:



def is_postalcode(elem):
    return (elem.attrib['k']== "addr:postcode")

def audit_postcode(postcode,postcodes):
    postcodes[postcode].add(postcode)
    return postcodes 

def update_postcode(postcode):
    #searching for 5 digits postcodes here and will return the ones that match
    search = re.match(r'^\d{5}$', postcode)
    try:
        print postcode 
    except:
        return postcode
    if search:
        clean_postcode = search.group(1)
        print "clean_postcode"
        print clean_postcode
        return clean_postcode
    
    return postcode



    


# ###### creat the csv file 

# In[ ]:

# this is code I got from many refrrenc and I tried to change small thing to be mine :)

from shapeelem import shape_element 


OSM_PATH = "C:\Users\hp\Desktop\las-vegas_nevada.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE

    if element.tag == 'node':
        for attrib in element.attrib:
            if attrib in NODE_FIELDS:
                node_attribs[attrib] = element.attrib[attrib]
        
        for child in element:
            node_tag = {}
            if LOWER_COLON.match(child.attrib['k']):
                node_tag['type'] = child.attrib['k'].split(':',1)[0]
                node_tag['key'] = child.attrib['k'].split(':',1)[1]
                node_tag['id'] = element.attrib['id']
                node_tag['value'] = child.attrib['v']
                if child.attrib['k'] == 'addr:street':
                        node_tag["value"] = update_name(child.attrib["v"],mapping)
                if child.attrib['k']=='addr:postcode':
                    node_tag["value"]=update_postcode(child.attrib["v"])
                tags.append(node_tag)
            elif PROBLEMCHARS.match(child.attrib['k']):
                continue
            else:
                node_tag['type'] = 'regular'
                node_tag['key'] = child.attrib['k']
                node_tag['id'] = element.attrib['id']
                node_tag['value'] = child.attrib['v']
                tags.append(node_tag)
        
        return {'node': node_attribs, 'node_tags': tags}
        
    elif element.tag == 'way':
        for attrib in element.attrib:
            if attrib in WAY_FIELDS:
                way_attribs[attrib] = element.attrib[attrib]
        
        p = 0
        for child in element:
            way_tag = {}
            way_node = {}
            
            if child.tag == 'tag':
                if LOWER_COLON.match(child.attrib['k']):
                    way_tag['type'] = child.attrib['k'].split(':',1)[0]
                    way_tag['key'] = child.attrib['k'].split(':',1)[1]
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child.attrib['v']
                    if child.attrib['k'] == 'addr:street':
                        way_tag["value"] = update_name(child.attrib["v"],mapping)
                    if child.attrib['k']=='addr:postcode':
                    node_tag["value"]=update_postcode(child.attrib["v"])
                    tags.append(way_tag)
                elif PROBLEMCHARS.match(child.attrib['k']):
                    continue
                else:
                    way_tag['type'] = 'regular'
                    way_tag['key'] = child.attrib['k']
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child.attrib['v']
                    tags.append(way_tag)
                    
            elif child.tag == 'nd':
                way_node['id'] = element.attrib['id']
                way_node['node_id'] = child.attrib['ref']
                way_node['position'] = p
                p += 1
                way_nodes.append(way_node)
        
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])



process_map(OSM_PATH, validate=False)


# ###### building database 

# In[ ]:

#from many refrence :)

import csv, sqlite3

con = sqlite3.connect("las_vegas.db")
con.text_factory = str
cur = con.cursor()

# create nodes table
cur.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp);")
with open('nodes.csv','rb') as nod:
    dr = csv.DictReader(nod) 
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp'])              for i in dr]

cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp)                 VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()

#create nodes_tags table
cur.execute("CREATE TABLE nodes_tags (id, key, value, type);")
with open('nodes_tags.csv','rb') as nod_tag:
    dr = csv.DictReader(nod_tag) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
con.commit()

#Create ways table
cur.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")
with open('ways.csv','rb') as way:
    dr = csv.DictReader(way) 
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
con.commit()

#Create ways_nodes table
cur.execute("CREATE TABLE ways_nodes (id, node_id, position);")
with open('ways_nodes.csv','rb') as way_nod:
    dr = csv.DictReader(way_nod) 
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db)
con.commit()

#Create ways_tags table
cur.execute("CREATE TABLE ways_tags (id, key, value, type);")
with open('ways_tags.csv','rb') as way_tag:
    dr = csv.DictReader(way_tag) 
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
con.commit()


# ###### sample file 

# In[ ]:

### sample 

from sample import get_element

#!/usr/bin/env python
# -*- coding: utf-8 -*-

  # Use cElementTree or lxml if too slow

OSM_FILE = "C:\Users\hp\Desktop\las-vegas_nevada.osm"  # Replace this with your osm file
SAMPLE_FILE = "sample.osm"

k = 10 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    #Reference:
    #http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """Yield element if it is the right type of tag

    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')


# ######  the size of file and count node and way 

# In[ ]:

import csv, sqlite3
con = sqlite3.connect("las_vegas.db")
con.text_factory = str
cur = con.cursor()
nodes = cur.execute('SELECT COUNT(*) FROM nodes')
nodes.fetchone()[0]


# In[ ]:

ways = cur.execute('SELECT COUNT(*) FROM ways')
ways.fetchone()[0]


# In[ ]:

### Popular cuisines


cur.execute("SELECT nodes_tags.value, COUNT(*) as num            FROM nodes_tags                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value = 'restaurant')                i ON nodes_tags.id = i.id            WHERE nodes_tags.key = 'cuisine'           GROUP BY nodes_tags.value           ORDER BY num DESC LIMIT 10;")

cur.fetchall()


# In[ ]:

users= cur.execute('SELECT user, COUNT(*) as num             FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e             GROUP BY user             ORDER BY num DESC              LIMIT 10')
users.fetchall()


# In[ ]:

##
users= cur.execute('SELECT timestamp, COUNT(*) as num             FROM nodes e             GROUP BY timestamp             ORDER BY num               LIMIT 5')
users.fetchall()


# In[ ]:

cur.execute("SELECT nodes_tags.value, COUNT(*) as num            FROM nodes_tags                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value = 'tower')                i ON nodes_tags.id = i.id            WHERE nodes_tags.key = 'power'           GROUP BY nodes_tags.value           ORDER BY num DESC LIMIT 5;")

cur.fetchall()

