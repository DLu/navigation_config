from navigation_config.topic_manager import topic_scan

class Configuration:
    def __init__(self):
        self.maps = {}
        self.observation_sources = {}
        self.paths = {}
        self.pose_array = None
        self.footprint = None
        self.goal = None
        
        topic_scan(self)
        
    def laser_scans(self):
        scans = []
        for source, d in self.observation_sources.iteritems():
            if 'LaserScan' in d['type']:
                scans.append(source)
        return scans
