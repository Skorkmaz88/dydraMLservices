## Data feeder
## Goals of data source classes are imitating different
## Machine Learning application scenarios easily
## TODO: Add different types of data, and distributions 
import time
import numpy as np
import requests
import json
import codecs, json 
import os




class StreamingDataSource(object):
    """A random data generator in streaming fashion 

    Attributes:
        upload_frequency    : An integer represents call for upload per second
        number_of_dimensions: An integer number of dimensions of each sample
        sampling_size       : An integer denotes number of sampled instance at each upload, 
                              it is expected that upload data won't be hard real time
        communication_type  : What protocol to be followed for uploading data
        upload_type         : Format of data for upload protocol 
        name                : Name for visualization and reporting purposes, e.g. sensor_name
        endpoint            : Communicaton endpoint 

    """
    
    
    upload_frequency  = 1
    number_of_dimensions = 1
    number_of_sensors = 100
    communication_type = 'HTTP'
    upload_type = 'JSON'
    name = ''
    endpoint = ''

    def __init__(self, name  = 'StreamingDataSensor', endpoint = 'http://localhost:5000/stream/api/v0.1'):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.name = name
        self.endpoint = endpoint


    def start(self):
        """Starts the simulation with """
        # !! TODO: Develop a more elegant approach 
        while True:
            self.__push__()
            # Better not to have so many more  than one request per second
            time.sleep(1.0 / self.upload_frequency)

    
    def __push__(self):
        # Sample the random data y
        output, timestamp =  self.__sample__()
        
        print output
        print timestamp
        data  = output.tolist()
        pair = []
        for i in range(0, self.number_of_sensors):
            pair.append([data[i], timestamp])
        
        bucket = {}
        
        bucket['data'] = json.dumps(data)
        # Call post for upload 
        print bucket
        #r = requests.post(self.endpoint,  json= bucket)
        # Push to the file 
        #self.write('FILE', pair[0])
        self.write('HTTP_TEST_FILE', pair)
        
    def write(self,choice, data):
        """ Different create options:
             FILE: Grafana graph ready file for JSON
             HTTP_TEST_FILE: File format used in Dydra-HTTP-Test repository
             TODO:
             HTTP: N-Quad call for adding graph data
             JSON: Standard JSON object for datafields and values
             MQTT: Push data points as MQTT payload as in N-QUAD
        """
              
        if choice == 'FILE':
            append_write = ''
            loc = '/home/semih/dydraSimulations/outputSensors.dat'
            if os.path.exists(loc):
                append_write = 'a' # append if already exists
            else:
                append_write = 'w' # make a new file if not
            f = open(loc, append_write)
            f.write(str(data) + ";")
            f.flush()
        # Generate static files for http test program   
        elif choice == 'HTTP_TEST_FILE':
            append_write = ''
            loc = '/home/semih/dydraSimulations/outputHttpSensors100.dat'
            if os.path.exists(loc):
                append_write = 'a' # append if already exists
            else:
                append_write = 'w' # make a new file if not
            
            f = open(loc, append_write)
            for x in range(0, len(data) ):
                f.write(str(data[x][0]) + ',' + str(data[x][1]) +',')
            f.write('\n')        
            f.flush()
            
        # Output to the stdout
        else:
            print data[0] +','+ data[1]
            
            
        
        
    def __sample__(self):
        """Samples random data with standard distribution """
        mu, sigma = 0, 0.1
        timestamp = int(time.time()) * 1000
        data  = np.random.normal(mu, sigma, self.number_of_sensors)
        return data, timestamp
        


# Run

sds = StreamingDataSource()
sds.start()