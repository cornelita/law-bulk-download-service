import redis


r = redis.Redis(host='redis', port=6379)


def set_progress_data(key, value):
    r.set(f'P-{key}', value)


def get_progress_data_by_key(key):
    return r.get(f'P-{key}')


def set_download_data(key, value):
    r.set(f'D-{key}', value)


def get_download_data_by_key(key):
    return r.get(f'D-{key}')


def get_multiple_download_data_by_key(keys):
    keys_formatted = [f'D-{key}' for key in keys]
    return r.mget(keys_formatted)


def get_multiple_progress_data_by_key(keys):
    keys_formatted = [f'P-{key}' for key in keys]
    return r.mget(keys_formatted)


def get_multiple_download_and_progress_by_key(keys):
    download_data = get_multiple_download_data_by_key(keys)
    progress_data = get_multiple_progress_data_by_key(keys)
    print(progress_data)
    result = []

    for i in range(len(download_data)):
        if progress_data[i] is None:
            progress_data[i] = 0

        result.append({
            'id': keys[i],
            'data': f'Bulk Download {keys[i]}',
            'progress': progress_data[i]
        })
    return result


def delete_progress_and_download_data(key):
    r.delete(f'P-{key}', f'D-{key}')
