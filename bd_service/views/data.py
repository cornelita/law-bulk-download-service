from redis import Redis


r = Redis(host='redis', port=6379)


def set_progress_data(key, value):
    r.set(f'progress:{key}', value, ex=3600)


def get_progress_data_by_key(key):
    return r.get(f'progress:{key}')


def set_download_data(key, value):
    r.set(f'download:{key}', value, ex=3600)


def get_download_data_by_key(key):
    return r.get(f'download:{key}')


def get_multiple_download_data_by_key(keys):
    keys_formatted = [f'download:{key}' for key in keys]
    return r.mget(keys_formatted)


def get_multiple_progress_data_by_key(keys):
    keys_formatted = [f'progress:{key}' for key in keys]
    return r.mget(keys_formatted)


def delete_progress_and_download_data(key):
    r.delete(f'download:{key}', f'progress:{key}')
