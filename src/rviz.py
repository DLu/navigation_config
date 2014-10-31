#!/usr/bin/python

import yaml
import rospy
from navigation_config import Configuration
from resource_retriever import get
import tempfile

class RVizConfig:
    def __init__(self, base_file=None):
        if base_file:
            self.data = yaml.load( base_file )
        else:
            self.data = {}
            
    def add_display(self, name, class_name, topic=None, color=None, fields={}):
        print name, topic
        d = {'Name': name, 'Class': class_name, 'Enabled': True}
        if topic:
            d['Topic'] = topic
        if color:
            d['Color'] = '%d; %d; %d'%color
        d.update(fields)
        self.data['Visualization Manager']['Displays'].append(d)
        
    def set_tool_topic(self, name, topic):
        for m in self.data['Visualization Manager']['Tools']:
            if m.get('Class', '')==name:
                m['Topic'] = topic
                return
        
    def add_model(self, parameter='robot_description'):
        self.add_display('RobotModel', 'rviz/RobotModel', fields={'Robot Description': parameter})
        
    def add_map(self, topic='/map', name='Map'):
        self.add_display(name, 'rviz/Map', topic)
        
    def add_laserscan(self, topic='/base_scan', color=(46, 255, 0)):
        self.add_display(topic, 'rviz/LaserScan', topic, color, 
            {'Size (m)': .1, 'Style': 'Spheres', 'Color Transformer': 'FlatColor'})

    def add_pose_array(self, topic='/particlecloud'):
        self.add_display('AMCL Cloud', 'rviz/PoseArray', topic)
        
    def add_footprint(self, topic, color=(0,170,255)):
        self.add_display('Robot Footprint', 'rviz/Polygon', topic, color)
        
    def add_path(self, topic, name, color=None):
        self.add_display(name, 'rviz/Path', topic, color)

    def add_pose(self, topic):
        self.add_display('Current Goal', 'rviz/Pose', topic)
        
    def set_goal(self, topic):
        self.set_tool_topic('rviz/SetGoal', topic)
        
    def write(self, f):
        f.write(yaml.dump( self.data, default_flow_style=False))

r = RVizConfig(get('package://navigation_config/config/base.rviz'))
if rospy.has_param('/robot_description'):
    r.add_model()
    
c = Configuration()    
for topic, name in c.maps.iteritems():
    r.add_map(topic, name)

for l in c.laser_scans():
    r.add_laserscan(l)

for topic, name in c.paths.items():
    r.add_path(topic, name)
    
if c.goal:
    r.add_pose(c.goal)
    r.set_goal(c.goal)
    
#r.add_pose_array()
#r.add_footprint('/move_base_node/global_costmap/foot/robot_footprint')

temp = tempfile.NamedTemporaryFile()
r.write(temp)
temp.flush()

import subprocess
subprocess.call(['rosrun','rviz','rviz', '-d', temp.name])
temp.close()

