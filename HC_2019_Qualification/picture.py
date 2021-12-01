class Picture:
    VERTICAL = 0
    HORIZONTAL = 1

    def __init__(self, picture_id: int, raw_data: str):
        orientation, tag_count, *tags = raw_data.split()
        self.id = picture_id
        self.orientation = Picture.HORIZONTAL if orientation == 'H' else Picture.VERTICAL

        self.number_of_tags = int(tag_count)

        self.tags = set(tags)

    def __repr__(self):
        return f"Picture({self.orientation}, {self.number_of_tags}, {self.tags})"
   