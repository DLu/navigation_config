#!/usr/bin/python

import yaml
import rospy
from navigation_config import Configuration

class RVizConfig:
    def __init__(self, base_filename=None):
        if base_filename:
            self.data = yaml.load( open(base_filename))
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
        
    def write(self, fn):
        f = open(fn, 'w')
        f.write(yaml.dump( self.data, default_flow_style=False))
        f.close()
        

r = RVizConfig('config/base.rviz')
if rospy.has_param('/robot_description'):
    r.add_model()
    
c = Configuration()    
for topic, name in c.maps.iteritems():
    r.add_map(topic, name)

for l in c.laser_scans():
    r.add_laserscan(l)

for topic, name in c.paths.items():
    r.add_path(topic, name)
    
#r.add_pose_array()
#r.add_footprint('/move_base_node/global_costmap/foot/robot_footprint')
#r.add_pose('/move_base_node/current_goal')

fn = 'temp.rviz'
r.write(fn)

import subprocess
#subprocess.call(['rosrun','rviz','rviz', '-d', fn])


