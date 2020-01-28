class Callstack():
    def __init__(self):
        self.stack = [{}]

    def push(self):
        self.stack.append({})

    def pop(self):
        self.stack.pop()

    def add(self, id, value, quiet=False):
        if not isinstance(value, dict):
            raise ValueError("value must be pushed in dictionary format")
        if self.stack[-1].get(id):
            self.stack[-1][id].update(value)
            if not quiet:
                self.stack[-1][id]["trace"].append({"value": value.get("value"), "line": value["line"]})
        else:
            self.stack[-1][id] = value
            if not quiet:
                self.stack[-1][id]["trace"] = [{"value": value.get("value"), "line": value["line"]}]

    def find(self, id):
        result = self.stack[-1].get(id)
        if result == None:
            raise ValueError(f"undefined variable: {id}")
        return result

    def trace(self, id):
        result = self.stack[-1].get(id)
        if result == None:
            raise ValueError(f"undefined variable: {id}")
        for i in result["trace"]:
            value = i["value"]
            line = i["line"]
            print(f"{id} = {value} at line {line}")


    def __repr__(self):
        return "callstack >\n" + str(self.stack)

if __name__ == "__main__":
    stack = Callstack()
    stack.add('a', {'value': 1})
    assert stack.find('a') == {'value': 1}
    stack.add('a', {'value': 2})
    assert stack.find('a') == {'value': 2}
    stack.push()
    stack.add('a', {'value': 3})
    assert stack.find('a') == {'value': 3}
    stack.pop()
    assert stack.find('a') == {'value': 2}
    stack.pop()
    print(stack)