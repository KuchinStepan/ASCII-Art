import PIL
from PIL import Image
import numpy as np


def grayscale_pixel(pixel):
    return 0.2989 * pixel[0] + 0.5870 * pixel[1] + 0.1140 * pixel[2]


def get_symbol_by_brightness(brightness):
    return '.'


class AsciiConverter:
    def __init__(self):
        self.file_name = None
        self.image = None
        self.file_type = 'png'
        self.symbol_width = 0
        self.symbol_height = 0
        self.pixel_width = 0
        self.pixel_height = 0
        self.grayscale_image = []

    def load_image(self, file_name):
        try:
            with Image.open(file_name) as im:
                im.load()
                self.image = np.asarray(im)
                self.file_name = file_name
                self.file_type = file_name.split('.')[-1]
                self.symbol_height = len(self.image)
                self.pixel_height = self.symbol_height
                if self.symbol_height > 0:
                    self.symbol_width = len(self.image[0])
                    self.pixel_width = self.symbol_width
                self._norm_size()
        except FileNotFoundError:
            return False, 'not found!'
        except PIL.UnidentifiedImageError:
            return False, 'in the wrong format!'
        except BaseException as e:
            raise e
        else:
            if len(self.image) == 0 or len(self.image[0]) == 0 or len(self.image[0][0]) < 3:
                return False, 'in the wrong format!'
            return True, 'successful'

    def get_output_file_name(self):
        folders = self.file_name.split('/')[:-1]
        path = '/'.join(folders)
        short_name = self.file_name.split('/')[-1].split('.')[0]
        # Написать добавления файла, если есть с таким именем
        return path + short_name + '.txt'

    def convert(self):
        self._convert_to_grayscale()
        block_width = self.pixel_width // self.symbol_width
        block_height = self.pixel_height // self.symbol_height
        output_file = self.get_output_file_name()
        with open(output_file, 'w') as f:
            for line in range(block_height):
                text_line = []
                for column in range(block_width):
                    symbol = get_symbol_by_brightness(self.grayscale_image[column][line])
                    text_line.append(symbol)
                f.write(''.join(text_line) + '\n')

    def _convert_to_grayscale(self):
        block_width = self.pixel_width // self.symbol_width
        block_height = self.pixel_height // self.symbol_height
        block_pixel_count = block_height * block_width

        self.grayscale_image = []
        block_width_index = 0
        block_height_index = 0
        while block_height_index < self.symbol_height:
            gray_line = []
            total_brightness = 0
            while block_width_index < self.symbol_width:
                for line in range(block_height):
                    for column in range(block_width):
                        total_brightness += grayscale_pixel(
                            self.image[block_height_index * block_height + line]
                                      [block_width_index * block_width + column]
                        )
                gray_line.append(total_brightness / block_pixel_count)
                block_width_index += 1
            self.grayscale_image.append(gray_line)
            block_width_index = 0
            block_height_index += 1

    def _norm_size(self):
        # scale = 10
        # min_value = min(self.symbol_height, self.symbol_width) // scale
        # if 20 < min_value < 50:
        #     scale = 30
        # elif 50 <= min_value:
        scale = min(self.symbol_height, self.symbol_width) // 250
        self.symbol_width = self.symbol_width // scale
        self.symbol_height = self.symbol_height // scale


if __name__ == '__main__':
    pass
