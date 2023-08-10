import unittest
import ascii_art


class TestAsciiArt(unittest.TestCase):
    def setUp(self):
        pass

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


if __name__ == '__main__':
    unittest.main()
