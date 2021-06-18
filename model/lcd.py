class Lcd:
    # def __init__(self, key_code, key_event, category, level, index, value, name):
    #     self._key_event = key_event
    #     self._key_code = key_code
    #     self._category = category
    #     self._level = level
    #     self._index = index
    #     self._value = value
    #     self._name = name

    _key_event = -1
    _key_code = -1
    _category = -1
    _level = -1
    _index = -1
    _value = -1
    _name = ''

    @property
    def key_event(self):
        return self._key_event

    @key_event.setter
    def key_event(self, key_event):
        self._key_event = key_event

    @property
    def key_code(self):
        return self._key_code

    @key_code.setter
    def key_code(self, key_code):
        self._key_code = key_code

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
