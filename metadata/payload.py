import json


class Payload:
    def __init__(self):
        self.received = ''
        self.publication_date = ''
        self.online_date = ''
        self.authors = List(Author)
        self.issues = Dict({'first': '', 'last': ''})
        self.keywords = List(str)
        self.references = ''
        self.language = ''
        self.journal_title = ''
        self.issn = ''
        self.doi = ''
        self.title = ''
        self.pages = Dict({'first': '', 'last': ''})
        self.publisher = ''
        self.volumes = Dict({'first': '', 'last': ''})


class Affiliation:
    def __init__(self, name):
        self.name = name


class Author:
    def __init__(self, surname='', firstname='', affiliations=None):
        self.firstname = firstname
        self.surname = surname
        self.affiliations = List(Affiliation)
        if affiliations:
            for institute in affiliations:
                self.affiliations.append(Affiliation(institute))


class Dict:
    def __init__(self, data):
        if type(data) is not dict:
            raise DictException('Can only handle dicts!')

        self.__dict__ = data


class List:
    def __init__(self, type):
        self.__type = type
        self.__data = []

    def append(self, item):
        if type(item) is self.__type:
            self.__data.append(item)
        else:
            raise ListException('Expect data-type: %s instead of %s' % (type(self.__type), type(item)))

    def __iter__(self):
        return self.__data.__iter__()

    def __getitem__(self, item):
        return self.__data.__getitem__(item)

    def __str__(self):
        return self.__data.__str__()

    def __repr__(self):
        return self.__data.__repr__()


class PayloadEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Payload):
            struct = obj.__dict__
            jsonable = self.__encode(struct)
            return jsonable
        return super().default(obj)

    def __encode(self, attribute):
        if type(attribute) is str or type(attribute) is int:
            return attribute
        elif type(attribute) is dict:
            return self.__encode_dict(attribute)
        elif type(attribute) is list:
            return self.__encode_list(attribute)
        elif isinstance(attribute, Dict):
            return self.__encode_dict(attribute.__dict__)
        elif isinstance(attribute, List):
            return self.__encode_list(attribute.__dict__)
        elif isinstance(attribute, Author):
            return self.__encode_dict(attribute.__dict__)
        elif isinstance(attribute, Affiliation):
            return self.__encode_dict(attribute.__dict__)

    def __encode_dict(self, attribute):
        new_dict = {}
        for key in attribute:
            new_dict[key] = self.__encode(attribute[key])
        return new_dict

    def __encode_list(self, attribute):
        new_list = []
        if type(attribute) is dict:
            for item in attribute['_List__data']:
                new_list.append(self.__encode(item))
        elif type(attribute) is list:
            for item in attribute:
                new_list.append(self.__encode(item))
        return new_list


class ListException(Exception):
    pass


class DictException(Exception):
    pass


class EncoderException(Exception):
    pass

    # class PayloadDecoder(json.JSONDecoder):
    #     def decode(self, s, _w=WHITESPACE.match):
    #         return super().decode(s, _w)
