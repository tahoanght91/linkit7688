class Lcd:
    _key_event = -1
    _key_code = -1
    _category = -1
    _level = -1
    _index_level1 = -1
    _index_level2 = -1
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
    def index_level1(self):
        return self._index_level1

    @index_level1.setter
    def index_level1(self, index_level1):
        self._index_level1 = index_level1

    @property
    def index_level2(self):
        return self._index_level2

    @index_level2.setter
    def index_level2(self, index_level2):
        self._index_level2 = index_level2

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
