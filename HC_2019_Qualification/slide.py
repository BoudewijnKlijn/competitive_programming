from HC_2019_Qualification.picture import Picture


class Slide:
    def __init__(self, pictures: [Picture]):
        self.pictures = pictures

    @property
    def tags(self):
        return set().union(*[p.tags for p in self.pictures])

    @property
    def n_tags(self):
        return len(self.tags)
