import redis
import argparse, pprint
import uuid
import os, sys, pprint
from google.cloud import redis_v1
from subprocess   import check_output
from mimesis      import Generic, locales

# Placeholder env vars
FROM_BYTES=104857
BASE_SIZE=250

class MemorystoreClient():
    def __init__(self, hostname=None, port=6379, database=None):
        self.hostname=hostname
        self.port=port
        self.database=database
        if database is None:
            self.r=redis.Redis(host=self.hostname, port=self.port)
        else:
            self.r=redis.Redis(host=self.hostname, port=self.port, db=self.database)

    def instanceSize(self):
        return self.r.info()['used_memory']

    def info(self):
        return self.r.info()

    def set(self, key, value):
        self.r.set(key, value)

    def get(self, key):
        return self.r.get(key)

    def mset(self, mapping):
        self.r.mset(mapping)

    def mget (self):
        pass

    def lpush(self, name, values):
        self.r.lpush(name, values)
        
    def lrange(self, name, start, end):
        return self.r.lrange(name, start, end)


class GenerateRandomData(object):
    
    @classmethod
    def DataGenerator(cls):
        pass

    @classmethod
    def generate(cls, client, size):
        pass
    @classmethod
    def checkInstanceSize(cls, redis_client):
        info = redis_client.r.info()
        return info["used_memory"]


class TestGenerator(object):
    
    @classmethod
    def test(cls, redis_client, memorystore_client=None, size=None):
        initial_size = redis_client.instanceSize()
        g = Generic(locales.EN)
        for i in range(int(size)):
            key = str(uuid.uuid4())
            value = g.person.name()
            redis_client.lpush(key, value)
            value = g.person.surname() 
            redis_client.lpush(key, value)
            value = g.address.address() 
            redis_client.lpush(key, value)
            value = g.science.dna_sequence()
            redis_client.lpush(key, value)

        final_size = redis_client.instanceSize()
        end_size = final_size - initial_size
        print(end_size)
        return end_size

    @classmethod
    def size_to_byte(cls, size):
        pass

def parseSize(size, data_ext=tuple(["M", "G", "T"])):
    arg_in = size[-1]
    pwr = data_ext.index(arg_in)
    to_bytes = int(size[:-1])*(1024**(2 + pwr))
    number_of_iterations = int(to_bytes/BASE_SIZE)
    return number_of_iterations


if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description='Redis client to connect to Memorystore')
    
    parser.add_argument('--instance', '-i', 
                        dest='instance', 
                        required=True,
                        help='(REQUIRED) Memorystore instance ID, used to retrieve instance metadata. Overriden by hostname and port.')

    parser.add_argument('--location', '-l', 
                        dest='location', 
                        required=True,
                        help='(REQUIRED) Memorystore instance location region. I.e. europe-west2.')

    parser.add_argument('--project',
                        dest='project', 
                        required=False, 
                        default=check_output('gcloud config get-value project', shell=True)[:-1].decode('utf-8'),
                        help='Memorystore instance project location. Defaults to the one in the gcloud environment.')

    parser.add_argument('--host', '--hostname', 
                        dest='hostname', 
                        required=False,
                        help='Hostname: IP address of the Memorystore instance.')
    
    parser.add_argument('--port', '-p', 
                        dest='port', 
                        required=False, 
                        default=6379,
                        help='Port of the Memorystore instance.')

    parser.add_argument('--generate-data', 
                        required=False, 
                        dest='generate',
                        help='''Generate fake data in the Memorystore instance. Requires the value of the size of the data generated.
                             Data format should be in SI format: 10M, 20G, 30T. (See https://physics.nist.gov/cuu/Units/binary.html)''')

    parser.add_argument('--database', '-db', 
                        dest='db', 
                        required=False, 
                        help='Database to connect the Redis client to.')

    parser.add_argument('--info',
                        action='store_true',
                        required=False, 
                        help='Show Memorystore database Redis info.')

    parser.add_argument('--test',
                        action='store_true',
                        required=False, 
                        help='Perform tests.')


    parser.add_argument('--load',
                        dest='load',
                        required=False, 
                        help='Perform load test.')

    args = parser.parse_args()

    if not args.hostname:
        try:
            memorystore_client = redis_v1.CloudRedisClient()
        except Exception as e:
            print(str(e))
            sys.exit(0)

        name = 'projects/{}/locations/{}/instances/{}'.format(args.project, args.location, args.instance)
        instance = memorystore_client.get_instance(name=name)
        hostname = instance.host
        port = instance.port

    else:
        hostname = args.hostname
        port = args.port
    
    try:
        db = args.db
    except:
        db = 0


    redis_client = MemorystoreClient(hostname=hostname, port=port, database=db)

    generate_data_ext = tuple(["M", "G", "T"])

    if args.generate and not args.load:
        assert args.generate.endswith(generate_data_ext), "Please check the data to generate format here: https://physics.nist.gov/cuu/Units/binary.html"
        if not args.hostname:
            if args.test:
                average = 0
                N_ITER = 1000
                for i in range(N_ITER):
                    size = TestGenerator.test(redis_client=redis_client, memorystore_client=memorystore_client, size=1)
                    average += size
                print(average/N_ITER)

            else:
                TestGenerator.test(redis_client=redis_client, memorystore_client=memorystore_client, size=parseSize(args.generate))

        else:
            TestGenerator.test(redis_client, size=args.generate[:-1])


    if args.info:
        instance_info = redis_client.info()
        pprint.pprint(instance_info)

    if args.load:
        if not args.generate:
            raise Exception('missing --generate argument')
        #pool_arguments = [(redis_client, memorystore_client, 100000, ) for i in range(int(args.load))]
        iterations = parseSize(args.generate)
        print(iterations)
        from multiprocessing import Process
        for worker in range(int(args.load)):
            print("Started worker " + str(worker))
            p = Process(target=TestGenerator.test, args=(redis_client, memorystore_client, iterations))
            p.start()
            #p.join()

