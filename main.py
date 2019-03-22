import redis
import argparse
from google.cloud import redis_v1
import os, sys
from subprocess import call

class MemorystoreClient():
    def __init__(self, hostname=None, port=6379, database=None):
        self.hostname=hostname
        self.port=port
        self.database=database
        if database is None:
            self.instance=redis.Redis(host=self.hostname, port=self.port)
        else:
            self.instance=redis.Redis(host=self.hostname, port=self.port, db=self.database)
    
    def Client():
       pass 
        

class GenerateRandomData(object):
    
    @classmethod
    def DataGenerator(cls):
        pass

    @classmethod
    def generate(cls):
        pass

    @classmethod
    def checkInstanceSize(cls):
        pass


if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description='Redis client to connect to Memorystore')
    
    parser.add_argument('--instance', '-i', dest='instance', required=True,
                        help='Memorystore instance ID, used to retrieve instance metadata. Overriden by hostname and port')

    parser.add_argument('--location', '-l', dest='location', required=True,
                        help='Memorystore instance location region. I.e. europe-west2')

    parser.add_argument('--project', dest='project', required=False, default=call('gcloud config get-value project', shell=True),
                        help='Memorystore instance project location. Defaults to the one in the gcloud environment')

    parser.add_argument('--host', '--hostname', dest='hostname', required=False,
                        help='Hostname: IP address of the Memorystore instance')
    
    parser.add_argument('--port', '-p', dest='port', required=False, default=6379,
                        help='Port of the Memorystore instance.')

    parser.add_argument('--generate-data', required=False, dest='generate-data-size',
                        help='Generate fake data in the Memorystore instance. Requires the value of the size of the data generated')

    parser.add_argument('--database', '-db', dest='db', required=True, 
                        help='Database to connect the Redis client to')

    args = parser.parse_args()

    if not args.hostname:
        try:
            memorystore_client = redis_v1.CloudRedisClient()
        except Exception as e:
            print(str(e))
            sys.exit(0)
        
        name = 'projects/{}/locations/{}/instances/{}'.format(args.project, args.location, args.instance)
        instance = memorystore_client.get_instance(name=args.instance)
        hostname = instance.host
        port = instance.port

    else:
        hostname = args.hostname
        port = args.port
        db=args.db
    print(args.project)
    print(hostname)
    client = MemorystoreClient(hostname=hostname, port=port, database=db)
