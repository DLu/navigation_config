import rostopic
import rosgraph
import rosgraph.impl.graph
import collections

def topic_scan(config):
    g = rosgraph.impl.graph.Graph()
    g.update()

    topics = map(str.strip, g.nt_nodes)
    subs = collections.defaultdict(list)
    pubs = collections.defaultdict(list)
    for edge in g.nt_all_edges:
        src = edge.start.strip()
        dest = edge.end.strip()
        if src in topics:
            subs[src] = dest
        if dest in topics:
            pubs[dest] = src
    
    for topic in topics:
        type_name = rostopic.get_topic_type(topic)[0]
        if type_name=='sensor_msgs/PointCloud2' or type_name=='sensor_msgs/LaserScan':
            config.observation_sources[topic] = {'type': type_name}
        elif type_name=='nav_msgs/OccupancyGrid':
            base = topic.split('/')[-1]
            if base == 'costmap':
                if 'local' in topic:
                    config.maps[topic] = 'Local Costmap'
                else:
                    config.maps[topic] = 'Global Costmap'
            else:
                config.maps[topic] = 'Map'
        elif type_name=='nav_msgs/Path':
            config.paths[topic] = 'Path'
        elif type_name=='geometry_msgs/PoseStamped':
            if topic in subs:
                config.goal = topic
    
    
"""    
nodes = g.nn_nodes

#print g.nt_edges

for a in g.nt_edges:
    #print a.label, a.key, a.rkey, a.start, a.end
    if 'move_base' in str(a):
        print a

         	end
 	key
 	label
 	rkey
 	start


#for topic in topics:
#    print rostopic.get_topic_type(topic.strip())    

        """
