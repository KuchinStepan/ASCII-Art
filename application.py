import tkinter as ttk
from tkinter import filedialog as fd
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
        self._make_file_open_frame()
        self._load_label = None
        self._set_load_result_text('Image is not selected')

    def _set_load_result_text(self, text, colour=BLACK):
        if self._load_label is not None:
            self._load_label.destroy()
        self._load_label = self._load_label = ttk.Label(self.root, text=text, bg=WHITE, fg=colour, font=40)
        self._load_label.place(relx=0.15, rely=0.25, relwidth=0.7, relheight=0.1)

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
            successful, message = self.converter.load_image(file_name)
            short_name = file_name.split('/')[-1]
            if len(short_name) > 15:
                short_name = short_name[:13] + '...'
            if successful:
                self._set_load_result_text(f'Image {short_name} selected')
                self._update_width_and_height()
            else:
                self._set_load_result_text(f'Image {short_name} {message}', RED)

    def _convert(self):
        self.converter.convert()

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
        self.width_entry.bind('<KeyPress>', _only_int_selector)
        self.width_entry.place(relx=0.1 + ENTRY_WIDTH, rely=ELEMENTS_SHIFT,
                               relwidth=ENTRY_WIDTH, relheight=ENTRY_HEIGHT)

        # Ввод высоты
        height_text = ttk.Label(frame, text='Height (symb)', bg=LIGHT_BLUE, font=40)
        height_text.place(relx=0.1, rely=ELEMENTS_SHIFT * 2 + ENTRY_HEIGHT,
                          relwidth=ENTRY_WIDTH, relheight=ENTRY_HEIGHT)

        self.height_entry = ttk.Entry(frame, bg='white', font=30)
        self.height_entry.bind('<KeyPress>', _only_int_selector)
        self.height_entry.place(relx=0.5, rely=ELEMENTS_SHIFT * 2 + ENTRY_HEIGHT,
                                relwidth=ENTRY_WIDTH, relheight=ENTRY_HEIGHT)

        button = ttk.Button(frame, text='Convert to txt', command=self._convert)
        button.place(relx=ENTRY_WIDTH / 2 + 0.1, rely=ELEMENTS_SHIFT * 3 + ENTRY_HEIGHT * 2,
                     relwidth=ENTRY_WIDTH, relheight=ENTRY_HEIGHT)

        self._update_width_and_height()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    pass
