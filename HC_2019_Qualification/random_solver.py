from random import Random

from HC_2019_Qualification.input_data_2019_q import Pictures
from HC_2019_Qualification.picture import Orientation
from HC_2019_Qualification.slide import Slide
from HC_2019_Qualification.slides import Slides
from valcon.strategy import Strategy


class RandomStrategy(Strategy):
    def __init__(self, seed: int):
        self.seed = seed

    def solve(self, input_data: Pictures) -> Slides:

        slides = []

        rng = Random(self.seed)

        vertical_picture = None

        for picture in input_data.pictures:
            if picture.orientation == Orientation.HORIZONTAL:
                slides.append(Slide([picture]))
            elif vertical_picture:
                slides.append(Slide([vertical_picture, picture]))
                vertical_picture = None
            else:
                vertical_picture = picture

        rng.shuffle(slides)
        return Slides(slides)
