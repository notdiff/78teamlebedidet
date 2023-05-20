from kivy.lang import Builder
from kivymd.app import MDApp
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from kivy.core.window import Window
from PIL import Image, ImageOps
import neiroset

root = Tk()
root.withdraw()

KV = """
Screen:
    MDSmartTile:
        id: bg
        radius: 0
        box_color: 0, 0, 0, .0
        source: "images/bg_image.png"
        size_hint: (1, 1)

    MDSmartTile:
        id: img1
        radius: 15
        box_radius: [15, 15, 15, 15]
        box_color: 0, 0, 0, .0
        source: "images/photo_2023-04-13_20-14-45.png"
        pos_hint: {"center_x": .3, "center_y": .5}
        size_hint: None, None
        size: "580dp", "380dp"
        on_release: app.open_file_chooser()

    MDSmartTile:
        id: img2
        radius: 15
        box_radius: [15, 15, 15, 15]
        box_color: 0, 0, 0, .0
        source: "images/photo_2023-04-13_20-14-45.png"
        pos_hint: {"center_x": .8, "center_y": .69}
        size_hint: None, None
        size: "340dp", "190dp"
        on_release: app.open_file_chooser()

    MDLabel:
        id: text_my
        halign: "center"
        text: ""
        bold: True
        pos_hint: {"center_x": .85, "center_y": .25}
        size_hint: (0.5, 0.3)
        color: 1, 1, 1, 1

    MDFillRoundFlatButton:
        id: but
        text: 'Выбрать изображение'
        pos_hint: {"center_x": .85, "center_y": .1}
        on_release: app.open_file_chooser()
        size_hint: (0.25, 0.1)
        text_color: 1, 1, 1, 1
        md_bg_color: 252.0/255, 109.0/255, 255.0/255, 1
"""

Window.size = (900, 500)

class MyApp(MDApp):
    title = 'Подсчет лебедей на фото'
    icon = 'images/icon.png'

    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_string(KV)

    def open_file_chooser(self):
        image_path = askopenfilename()
        if not image_path:
            return
        self.handle(image_path)

    def _on_file_drop(self, window, file_path):
        image_path = str(file_path)[2:][:-1]
        self.handle(image_path)

    def on_start(self):
        image = Image.open("images/prev.png")
        width, height = image.size
        max_width = 480
        max_height = 380

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)

        width, height = image.size
        self.root.ids.img1.size = (str(width) + "dp", str(height) + "dp")
        self.root.ids.img1.source = "images/prev.png"

        image = Image.open("images/photo_2023-04-13_20-14-45.png")
        width, height = image.size

        max_width = 340
        max_height = 190
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
        width, height = image.size

        self.root.ids.img2.size = (str(width) + "dp", str(height) + "dp")
        self.root.ids.img2.source = "images/photo_2023-04-13_20-14-45.png"

    def handle(self, image_path):
        if image_path.split('.')[-1] not in ["bmp", "jpg", "jpeg", "png"]:
            return
        image = Image.open(image_path)

        width, height = image.size
        max_width = 480
        max_height = 380

        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)

        width, height = image.size

        ph, ans = neiroset.gen(image_path)

        self.root.ids.img1.size = (str(width) + "dp", str(height) + "dp")
        self.root.ids.img1.source = ph

        self.root.ids.text_my.text = ans

        width, height = image.size
        max_width = 340
        max_height = 190
        if width > max_width or height > max_height:
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
        width, height = image.size

        self.root.ids.img2.size = (str(width) + "dp", str(height) + "dp")
        self.root.ids.img2.source = image_path


if __name__ == '__main__':
    MyApp().run()
