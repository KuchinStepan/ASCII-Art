from PIL import Image, UnidentifiedImageError
from load_image_error import LoadImageError
import colorama
import numpy as np
import os


colorama.init(autoreset=True)


COMMON_SYMBOL_COUNT = 60
ALPHABET = '  .-;?#@@'
ANSI_COLOURS = {(255, 0, 0): colorama.Fore.RED, (0, 255, 0): colorama.Fore.GREEN, (0, 0, 255): colorama.Fore.BLUE,
                (1, 1, 1): colorama.Fore.BLACK, (230, 230, 230): colorama.Fore.WHITE,
                (255, 255, 0): colorama.Fore.YELLOW, (0, 204, 204): colorama.Fore.CYAN,
                (204, 0, 204): colorama.Fore.MAGENTA}


def grayscale_pixel(pixel):
    return 0.2989 * (pixel[0] / 256) + 0.5870 * (pixel[1] / 256) + 0.1140 * (pixel[2] / 256)


def get_symbol_by_brightness(brightness):
    symbol = ALPHABET[::-1][int(brightness * len(ALPHABET) - 1e-9)]
    return symbol


def get_vectors_difference(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2) ** 0.5


def get_ansi_colour_by_pixel(pixel):
    symbol_colour = colorama.Fore.WHITE
    min_value = 10000000
    for colour in ANSI_COLOURS.keys():
        value = get_vectors_difference(colour, pixel)
        if value < min_value:
            min_value = value
            symbol_colour = ANSI_COLOURS[colour]
    return symbol_colour


def get_coloured_symbol(pixel):
    symbol = get_symbol_by_brightness(grayscale_pixel(pixel))
    colour = get_ansi_colour_by_pixel(pixel)
    return colour + colorama.Back.WHITE + symbol


def _are_same_scales(pixel_width, pixel_height, symbol_width, symbol_height):
    result = (pixel_width / symbol_width) * (pixel_height / symbol_height)
    return abs(result - 1) < 0.2


class AsciiConverter:
    def __init__(self):
        self.file_name = None
        self.image_array = None
        self.file_type = 'png'
        self.symbol_width = 0
        self.symbol_height = 0
        self.pixel_width = 0
        self.pixel_height = 0
        self.grayscale_image = []
        self.pil_image = None
        self.output_file_name = None
        self.coloured = False

    def load_image(self, file_name):
        try:
            with Image.open(file_name) as im:
                im.load()
                self.pil_image = im
                self.image_array = np.asarray(im)
                self.file_type = file_name.split('.')[-1]
                self.symbol_height = len(self.image_array)
                self.pixel_height = self.symbol_height
                if self.symbol_height > 0:
                    self.symbol_width = len(self.image_array[0])
                    self.pixel_width = self.symbol_width
                self._norm_size()
        except FileNotFoundError:
            raise LoadImageError('not found!')
        except UnidentifiedImageError:
            raise LoadImageError('in the wrong format!')
        except BaseException as e:
            raise LoadImageError(f'has unknown error: {e}')
        else:
            if len(self.image_array) == 0 or len(self.image_array[0]) == 0 or len(self.image_array[0][0]) < 3:
                raise LoadImageError('in the wrong format!')
            self.file_name = file_name

    def _set_output_file_name(self):
        folders = self.file_name.split('/')[:-1]
        path = '/'.join(folders)
        short_name = self.file_name.split('/')[-1].split('.')[0]
        coloured = '_coloured' if self.coloured else ''
        file_name = path + '/' + short_name + coloured + '.txt'
        i = 1
        while os.path.exists(file_name):
            file_name = path + '/' + short_name + f'({i})' + coloured + '.txt'
            i += 1
        self.output_file_name = file_name

    def convert(self):
        self._set_output_file_name()
        self.symbol_height = min(self.pixel_height, self.symbol_height)
        self.symbol_width = min(self.pixel_width, self.symbol_width)
        with Image.open(self.file_name) as im:
            im.load()
            self.pil_image = im
            self.image_array = np.asarray(self.pil_image)
            self._reduce_image_array()
        if not self.coloured:
            self._convert_to_grayscale()
        with open(self.output_file_name, 'w', encoding='ANSI') as f:
            for line in range(self.symbol_height):
                for column in range(self.symbol_width):
                    if self.coloured:
                        symbol = get_coloured_symbol(self.image_array[line][column])
                    else:
                        symbol = get_symbol_by_brightness(self.grayscale_image[line][column])
                    f.write(symbol)
                f.write('\n')
        # os.startfile('/'.join(self.output_file_name.split('/')[:-1]) + '/')
        if not self.coloured:
            os.startfile(self.output_file_name)

    def _reduce_image_array(self):
        if _are_same_scales(self.pixel_width, self.pixel_height, self.symbol_width, self.symbol_height):
            return
        block_width = int(self.pixel_width / self.symbol_width) + 1
        block_height = int(self.pixel_height / self.symbol_height) + 1
        if block_height == 1 or block_width == 1:
            return

        new_array = []
        for y in range(self.symbol_height):
            row = []
            for x in range(self.symbol_width):
                sum_pixel = [0, 0, 0]
                pixel_count = 0
                for i in range(block_width):
                    current_x = x * block_width + i
                    if current_x >= len(self.image_array[0]):
                        break
                    for j in range(block_height):
                        current_y = y * block_height + j
                        if current_y >= len(self.image_array):
                            break
                        pixel_count += 1
                        for c in range(3):
                            sum_pixel[c] += self.image_array[current_y][current_x][c]
                if pixel_count != 0:
                    avg_pixel = [sum_pixel[0] // pixel_count, sum_pixel[1] // pixel_count,
                                 sum_pixel[2] // pixel_count]
                    row.append(avg_pixel)
                else:
                    row.append([255, 255, 255])
            new_array.append(row)
        self.image_array = new_array

    def recalculate_symbol_width(self):
        if self.file_name is None:
            return
        self.symbol_width = int(self.pixel_height / self.pixel_width * self.symbol_height * 9 / 8)

    def recalculate_symbol_height(self):
        if self.file_name is None:
            return
        self.symbol_height = int(self.pixel_width / self.pixel_height * self.symbol_width * 8 / 9)

    def _convert_to_grayscale(self):
        self.grayscale_image = []
        for line in range(self.symbol_height):
            gray_line = []
            for column in range(self.symbol_width):
                brightness = grayscale_pixel(self.image_array[line][column])
                gray_line.append(brightness)
            self.grayscale_image.append(gray_line)

    def _norm_size(self):
        scale = min(self.symbol_height, self.symbol_width) // COMMON_SYMBOL_COUNT
        if scale > 1 and scale != 0:
            self.symbol_width = self.symbol_width * 15 // scale // 8
            self.symbol_height = self.symbol_height // scale


if __name__ == '__main__':
    pass
