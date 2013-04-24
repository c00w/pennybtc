import redis

r = redis.StrictRedis(unix_socket_path='/tmp/redis.sock')

def get_connection():
    return r
