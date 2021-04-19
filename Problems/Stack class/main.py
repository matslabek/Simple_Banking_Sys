class Stack():

    def __init__(self, elements=None):
        if elements is None:
            elements = []
        self.elements = elements

    def push(self, el):
        self.elements.append(el)

    def pop(self):
        return self.elements.pop()

    def peek(self):
        return self.elements[-1]

    def is_empty(self):
        return bool(not self.elements)
