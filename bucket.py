import boto3

def upload_s3(voice_telegram_url, file_id):
    if(voice_telegram_url is None): return None

    file_name = file_id + '.ogg'
    client = boto3.client('s3')
    client.upload_file(voice_telegram_url, 'telegram-voices', file_name)

    bucket_location = client.get_bucket_location(Bucket='telegram-voices')
    return "https://s3-{0}.amazonaws.com/{1}/{2}".format(
        bucket_location['LocationConstraint'],
        'telegram-voices',
        file_name)

