import itertools

from HC_2019_Qualification.slide import Slide
from valcon import OutputData


class Slides(OutputData):

    def save(self, filename: str):
        pass

    def __init__(self, slides: []):
        if isinstance(slides[0], Slide):
            self.slides = slides
        elif isinstance(slides[0], Slides):
            self.slides = list(itertools.chain.from_iterable([slide.slides for slide in slides]))

    def __str__(self):
        return '\n'.join(str(slide) for slide in self.slides)

    def __add__(self, other):
        return Slides(self.slides + other.slides)

    def first_slide(self):
        return self.slides[0]

    def last_slide(self):
        return self.slides[-1]
