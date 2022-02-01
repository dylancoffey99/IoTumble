import boto3


class Session:
    def __init__(self, access_key_id, secret_access_key, region_name):
        self.session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name)

    def get_session(self):
        return self.session
