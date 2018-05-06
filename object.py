class Object:

    def __init__(self):
        self.x = None
        self.y = None
        self.components = dict()

    def get_component(self, component):
        return self.components[component] if component in self.components else None

