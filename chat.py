import redis
import json

REDIS_HOST = 'de.futoke.ru'
REDIS_PORT = 6379
PIPE_NAME = 'itmo'


def init_chat():
    conn = redis.StrictRedis(host=REDIS_HOST,
                    port=REDIS_PORT,
                    db=0,
                    username='default',
                    password='dark_chat',
                    decode_responses=True)
    reader = conn.pubsub()
    reader.subscribe(PIPE_NAME)
    return conn, reader

def send_msg(msg):
    conn.publish(PIPE_NAME, json.dumps(msg))
    print(msg)

def read_msgs(callback, frame_msgs):
    print('In read')
    for msg in reader.listen():
        if type(msg['data']) is int:
            continue
        print(msg)
        msg = json.loads(msg['data'])
        callback(frame_msgs, msg)
        # callback(frame_msgs, 
        #          f'{msg["nickname"]}:\n{msg["text"]}')

conn, reader = init_chat()