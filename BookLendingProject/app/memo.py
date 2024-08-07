
import json


class Memo(object):

    def __new__(clazz):
        if not hasattr(clazz, 'instance'):
            clazz.instance = super(Memo, clazz).__new__(clazz)
        return clazz.instance

    def __init__(self):
        self.memo = {}

    def save_snapshot(self):
        with open('memo.json', 'w') as file:
            file.write(json.dumps(self.memo, default=lambda o: o.__dict__, indent=4))

    def load_snapshot(self):
        with open('memo.json', 'r') as file:
            self.memo = json.load(file)

            if "COUNTER" not in self.memo:
                self.memo["COUNTER"] = 1


instance = Memo()
