from datetime import datetime

class CustomMapper():
    def map(self, source, target_class):
        target = target_class()
        for key, value in source.__dict__.items():
            if hasattr(target, key):
                setattr(target, key, value)
        return target

mapper = CustomMapper()

def timestamp():
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")

def as_dict(input):
    temp = None
    if isinstance(input, dict):
        temp = input
    else:
        temp = input.__dict__

    return temp