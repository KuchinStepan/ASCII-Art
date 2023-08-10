import unittest
import ascii_art


class TestAsciiArt(unittest.TestCase):
    def setUp(self):
        self.converter = ascii_art.AsciiConverter()
        self.converter.file_name = 'C:\\folder\\test.txt'
        self.converter.pixel_height = 440
        self.converter.pixel_width = 680

    def testWhiteGrayscalePixel(self):
        pixel = (255, 255, 255)
        result = ascii_art.grayscale_pixel(pixel)
        self.assertAlmostEqual(1, result, 2)

    def testGrayGrayscalePixel(self):
        pixel = (127, 127, 127)
        result = ascii_art.grayscale_pixel(pixel)
        self.assertAlmostEqual(0.5, result, 2)

    def testGetVectorsDifference(self):
        a = (127, 28, 39)
        b = (43, 130, 40)
        result = ascii_art.get_vectors_difference(a, b)
        self.assertAlmostEqual(132.14, result, 2)

    def testGetSymbolByBrightness(self):
        brightness = 0.49
        result = ascii_art.get_symbol_by_brightness(brightness)
        self.assertEqual(';', result)

    def testAnsiColourByPixel(self):
        pixel = (3, 230, 7)
        green = ascii_art.ANSI_COLOURS[(0, 255, 0)]
        result = ascii_art.get_ansi_colour_by_pixel(pixel)
        self.assertEqual(green, result)

    def testGetColouredSymbol(self):
        pixel = (35, 250, 6)
        result = ascii_art.get_coloured_symbol(pixel)
        self.assertEqual('\x1b[32m\x1b[47m-', result)

    def testSameScales(self):
        pixel_width = 100
        pixel_height = 93
        symbol_width = 101
        symbol_height = 92
        result = ascii_art._are_same_scales(pixel_width, pixel_height, symbol_width, symbol_height)
        self.assertTrue(result)

    def testSettingOutputFileName(self):
        self.converter._set_output_file_name()
        expected = '/C:\\folder\\test.txt'
        self.assertEqual(expected, self.converter.output_file_name)

    def testRecalculateSymbolWidth(self):
        self.converter.symbol_height = 110
        self.converter.recalculate_symbol_width()
        self.assertAlmostEqual(80, self.converter.symbol_width, -1)

    def testRecalculateSymbolHeight(self):
        self.converter.symbol_width = 80
        self.converter.recalculate_symbol_height()
        self.assertAlmostEqual(110, self.converter.symbol_height, -1)

    def testNormSize(self):
        self.converter.symbol_width = 680
        self.converter.symbol_height = 440
        self.converter._norm_size()
        self.assertAlmostEqual(182, self.converter.symbol_width, -1)
        self.assertAlmostEqual(62, self.converter.symbol_height, -1)


if __name__ == '__main__':
    unittest.main()
