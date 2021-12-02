from HC_2019_Qualification.slides import Slides
from valcon import InputData, OutputData
from valcon.Scorer import Scorer


class Scorer2019Q(Scorer):

    @staticmethod
    def _calculate_transition(slide_a, slide_b):
        intersection_size = len(slide_a.tags & slide_b.tags)
        set_minus_size = slide_a.n_tags - intersection_size
        set_minus_size_2 = slide_b.n_tags - intersection_size
        return min(intersection_size, set_minus_size, set_minus_size_2)

    def calculate(self, slides: Slides) -> int:
        score = 0
        for slide_a, slide_b in zip(slides.slides[:-1], slides.slides[1:]):
            score += self._calculate_transition(slide_a, slide_b)
        return score

    def __init__(self, input_data: InputData):
        pass
