def success(message, data=None):
    return {
        "status": True,
        "message": message,
        "data": data
    }, 200


def error(message):
    return {
        "status": False,
        "message": message
    }, 200
