from HC_2019_Qualification.slide import Slide
from valcon import OutputData


class Slides(OutputData):

    def save(self, filename: str):
        pass

    def __init__(self, slides: [Slide]):
        self.slides = slides

    def __str__(self):
        return '\n'.join(str(slide) for slide in self.slides)
