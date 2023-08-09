import tkinter as ttk
from tkinter import filedialog as fd
from load_image_error import LoadImageError
import ascii_art


SCREEN_HEIGHT = 500
SCREEN_WIDTH = 600

ENTRY_HEIGHT = 0.2
ENTRY_WIDTH = 0.4
ELEMENTS_SHIFT = 0.1

LIGHT_BLUE = '#afbaf5'
WHITE = '#fafafa'
BLACK = '#000000'
RED = '#cc2323'


def set_screen(root):
    root['bg'] = WHITE
    root.title('ASCII-Art')
    root.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}')
    root.resizable(width=False, height=False)


def set_symbols_count(entry_label, text):
    contents = ttk.StringVar()
    contents.set(text)
    entry_label['textvariable'] = contents


def _only_int_selector(event):
    return 'break' if event.keysym not in (list('1234567890') + ['BackSpace', 'Delete', 'Left', 'Right']) else ''


class Application:
    def __init__(self):
        self.root = ttk.Tk()
        self.converter = ascii_art.AsciiConverter()
        set_screen(self.root)
        self._make_pict_size_frame()
        self.file_name = None
        self.coloured = ttk.BooleanVar()
        self._make_file_open_frame()
        self._load_label = None
        self._convert_text_label = None
        self._set_load_result_text('Image is not selected')
        self.last_entry_type = None
        self._set_colour_checking()

    def _set_load_result_text(self, text, colour=BLACK):
        if self._load_label is not None:
            self._load_label.destroy()
        self._load_label = ttk.Label(self.root, text=text, bg=WHITE, fg=colour, font=40)
        self._load_label.place(relx=0.15, rely=0.25, relwidth=0.7, relheight=0.1)

    def _set_convert_result_text(self, text=None):
        if self._convert_text_label is not None:
            self._convert_text_label.destroy()
        if text == '':
            return
        short_name = self.converter.output_file_name.split('/')[-1]
        if len(short_name) > 15:
            short_name = short_name[:13] + '...'
        text = f'Successfully converted to {short_name}'
        self._convert_text_label = ttk.Label(self.root, text=text, bg=WHITE, font=40)
        self._convert_text_label.place(relx=0.15, rely=0.75, relwidth=0.7, relheight=0.1)

    def _set_colour_checking(self):
        button = ttk.Checkbutton(self.root, text='Coloured', variable=self.coloured,
                                 onvalue=True, offvalue=False, bg=WHITE)
        button.place(relx=0.15, rely=0.85, relwidth=0.7, relheight=0.1)

    def _update_width_and_height(self):
        set_symbols_count(self.height_entry, str(self.converter.symbol_height))
        set_symbols_count(self.width_entry, str(self.converter.symbol_width))

    def open_file(self):
        # initialdir = 'D:/'
        wanted_files = (
            ('IMAGES', '*.png;*.jpg;*.jpeg'),
            ('ALL', '*.*')
        )
        file_name = fd.askopenfilename(title='Select image', filetypes=wanted_files)
        if file_name != '':
            self.file_name = file_name
            short_name = file_name.split('/')[-1]
            if len(short_name) > 15:
                short_name = short_name[:13] + '...'
            try:
                self.converter.load_image(file_name)
            except LoadImageError as e:
                self._set_load_result_text(f'Image {short_name} {e.message}', RED)
                self.file_name = None
            else:
                self._set_load_result_text(f'Image {short_name} selected')
                self._update_width_and_height()
                self._set_convert_result_text('')

    def _convert(self):
        if self.file_name is None:
            return
        self.converter.coloured = self.coloured.get()
        self.converter.symbol_width = int(self.width_entry.get())
        self.converter.symbol_height = int(self.height_entry.get())
        self.converter.convert()
        self._set_convert_result_text()

    def _width_entry_last(self, e):
        self.last_entry_type = 'width'

    def _height_entry_last(self, e):
        self.last_entry_type = 'height'

    def _synchronize_size(self):
        if self.last_entry_type is None:
            return
        elif self.last_entry_type == 'height':
            height = self.height_entry.get()
            if height == '':
                return
            if int(height) > 0:
                self.converter.symbol_height = int(height)
                self.converter.recalculate_symbol_width()
        else:
            width = self.width_entry.get()
            if width == '':
                return
            if int(width) > 0:
                self.converter.symbol_width = int(width)
                self.converter.recalculate_symbol_height()
        self._update_width_and_height()

    def _make_file_open_frame(self):
        frame = ttk.Frame(self.root, bg=LIGHT_BLUE, bd=5)
        frame.place(relx=0.15, rely=0.1, relwidth=0.7, relheight=0.15)

        text = ttk.Label(frame, text='Select image', bg=LIGHT_BLUE, font=40)
        text.place(relx=0.1, rely=0.1, relwidth=ENTRY_WIDTH, relheight=0.8)

        button = ttk.Button(frame, text='Select', command=self.open_file)
        button.place(relx=0.1 + ENTRY_WIDTH, rely=0.25, relwidth=ENTRY_WIDTH, relheight=0.5)

    def _make_pict_size_frame(self):
        frame = ttk.Frame(self.root, bg=LIGHT_BLUE, bd=5)
        frame.place(relx=0.15, rely=0.4, relwidth=0.7, relheight=0.35)

        # Ввод ширины
        width_text = ttk.Label(frame, text='Width (symb)', bg=LIGHT_BLUE, font=40)
        width_text.place(relx=0.1, rely=ELEMENTS_SHIFT,
                         relwidth=ENTRY_WIDTH, relheight=ENTRY_HEIGHT)

        self.width_entry = ttk.Entry(frame, bg='white', font=30)
        self.width_entry.bind('<Key>', _only_int_selector)
        self.width_entry.bind('<Key>', self._width_entry_last, True)
        self.width_entry.place(relx=0.1 + ENTRY_WIDTH, rely=ELEMENTS_SHIFT,
                               relwidth=ENTRY_WIDTH, relheight=ENTRY_HEIGHT)

        # Ввод высоты
        height_text = ttk.Label(frame, text='Height (symb)', bg=LIGHT_BLUE, font=40)
        height_text.place(relx=0.1, rely=ELEMENTS_SHIFT * 2 + ENTRY_HEIGHT,
                          relwidth=ENTRY_WIDTH, relheight=ENTRY_HEIGHT)

        self.height_entry = ttk.Entry(frame, bg='white', font=30)
        self.height_entry.bind('<Key>', _only_int_selector)
        self.height_entry.bind('<Key>', self._height_entry_last, True)
        self.height_entry.place(relx=0.5, rely=ELEMENTS_SHIFT * 2 + ENTRY_HEIGHT,
                                relwidth=ENTRY_WIDTH, relheight=ENTRY_HEIGHT)

        sync_button = ttk.Button(frame, text='Synchronize', command=self._synchronize_size)
        sync_button.place(relx=0.2, rely=ELEMENTS_SHIFT * 3 + ENTRY_HEIGHT * 2,
                          relwidth=ENTRY_WIDTH - 0.2, relheight=ENTRY_HEIGHT)

        button = ttk.Button(frame, text='Convert to txt', command=self._convert)
        button.place(relx=ENTRY_WIDTH / 2 + 0.3, rely=ELEMENTS_SHIFT * 3 + ENTRY_HEIGHT * 2,
                     relwidth=ENTRY_WIDTH, relheight=ENTRY_HEIGHT)

        self._update_width_and_height()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    pass
