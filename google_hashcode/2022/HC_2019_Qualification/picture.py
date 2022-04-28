from enum import Enum


class Orientation(Enum):
    VERTICAL = 0
    HORIZONTAL = 1


class Picture:
    # holds an int value for each tag to reduce memory footprint and probably also increases performance
    # of some strategies
    dictionary = dict()

    def __init__(self, picture_id: int, raw_data: str):
        orientation, tag_count, *tags = raw_data.split()
        self.id = picture_id
        self.orientation = Orientation.HORIZONTAL if orientation == 'H' else Orientation.VERTICAL

        self.number_of_tags = int(tag_count)

        tag_indexes = set()
        for tag in tags:
            if tag not in Picture.dictionary:
                Picture.dictionary[tag] = len(Picture.dictionary)  # this works when countring from 0
            tag_indexes.add(Picture.dictionary[tag])

        self.tags = tag_indexes

    def __repr__(self):
        return f"Picture({self.id=}, {self.orientation=}, {self.number_of_tags})"
