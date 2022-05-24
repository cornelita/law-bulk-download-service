from redis import Redis


r = Redis(host='redis', port=6379)


def set_progress_data(key, value):
    r.set(f'{key}:P', value, ex=3600)


def get_progress_data_by_key(key):
    return r.get(f'{key}:P')


def set_download_data(key, value):
    r.set(f'{key}:D', value, ex=3600)


def get_download_data_by_key(key):
    return r.get(f'{key}:D')


def get_multiple_download_data_by_key(keys):
    keys_formatted = [f'{key}:D' for key in keys]
    return r.mget(keys_formatted)


def get_multiple_progress_data_by_key(keys):
    keys_formatted = [f'{key}:P' for key in keys]
    return r.mget(keys_formatted)


def get_multiple_download_and_progress_by_key(keys):
    download_data = get_multiple_download_data_by_key(keys)
    progress_data = get_multiple_progress_data_by_key(keys)
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
    r.delete(f'{key}:D', f'{key}:P')
