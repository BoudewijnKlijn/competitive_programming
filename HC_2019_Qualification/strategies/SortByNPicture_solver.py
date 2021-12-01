from HC_2019_Qualification.input_data_2019_q import Pictures
from HC_2019_Qualification.slide import Slide
from HC_2019_Qualification.slides import Slides
from valcon.strategy import Strategy


class SortByNPicturesStrategy(Strategy):
    def solve(self, input_data: Pictures) -> Slides:

        slides = []

        vertical_picture = None

        input_data.pictures = sorted(input_data.pictures, key=lambda x: x.number_of_tags)

        for picture in input_data.pictures:
            if picture.orientation == picture.HORIZONTAL:
                slides.append(Slide([picture]))
            elif vertical_picture:
                slides.append(Slide([vertical_picture, picture]))
                vertical_picture = None
            else:
                vertical_picture = picture

        return Slides(slides)
