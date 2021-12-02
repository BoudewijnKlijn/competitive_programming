from HC_2019_Qualification.picture import Picture


class Slide:
    def __init__(self, pictures: [Picture]):
        self.pictures = pictures

    def __str__(self):
        return 'Slide:\n\t' + '\n\t'.join([str(p) for p in self.pictures])

    @property
    def tags(self):
        return set().union(*[p.tags for p in self.pictures])

    @property
    def number_of_tags(self):
        return len(self.tags)
