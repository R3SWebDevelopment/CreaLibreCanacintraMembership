from datetime import datetime


def build_log(user, message):
    now = datetime.now()
    return {
        'user': user.pk,
        'timestamp': now.strftime('%Y%m%dT%H%M%S:%f %z'),
        'message': message
    }