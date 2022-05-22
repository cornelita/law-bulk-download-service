import redis


r = redis.Redis(host='redis', port=6379)


def set_progress_data(key, value):
    r.lpush(f'P-{key}', value)


def get_progress_data_by_key(key):
    return r.lrange(f'P-{key}', 0, -1)


def set_download_data(key, value):
    r.set(f'D-{key}', value)


def get_download_data_by_key(key):
    return r.get(f'D-{key}')


def delete_progress_and_download_data(key):
    r.delete(f'P-{key}', f'D-{key}')
