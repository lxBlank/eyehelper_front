import uuid

def getUid():
    data = uuid.uuid4().hex
    return data

print(getUid())