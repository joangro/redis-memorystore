# Redis-Memorystore

A python wrapper to use [redis-py](https://pypi.org/project/redis/) library with the [Memorystore Client Libraries](https://googleapis.github.io/google-cloud-python/latest/redis/index.html).

It includes a random data generator, using the [mimesis library](https://mimesis.readthedocs.io/), for testing purposes.

As it uses Mimesis, **it is required to use Python 3.6.X or higher.**

## Usage

1. Install dependencies:

`pip install -r requirements.txt`

2. Command help:

- Required flags:

`python main.py --instance  random-data-tests --location europe-west2`

- Full help:

`python main.py --help`

Output:

```
usage: main.py [-h] --instance INSTANCE --location LOCATION
               [--project PROJECT] [--host HOSTNAME] [--port PORT]
               [--generate-data GENERATE] [--database DB] [--info] [--test]

Redis client to connect to Memorystore

optional arguments:
  -h, --help            show this help message and exit
  --instance INSTANCE, -i INSTANCE
                        (REQUIRED) Memorystore instance ID, used to retrieve
                        instance metadata. Overriden by hostname and port.
  --location LOCATION, -l LOCATION
                        (REQUIRED) Memorystore instance location region. I.e.
                        europe-west2.
  --project PROJECT     Memorystore instance project location. Defaults to the
                        one in the gcloud environment.
  --host HOSTNAME, --hostname HOSTNAME
                        Hostname: IP address of the Memorystore instance.
  --port PORT, -p PORT  Port of the Memorystore instance.
  --generate-data GENERATE
                        Generate fake data in the Memorystore instance.
                        Requires the value of the size of the data generated.
                        Data format should be in SI format: 10M, 20G, 30T.
                        (See https://physics.nist.gov/cuu/Units/binary.html)
  --database DB, -db DB
                        Database to connect the Redis client to.
  --info                Show Memorystore database Redis info.
  --test                Perform tests.
```
