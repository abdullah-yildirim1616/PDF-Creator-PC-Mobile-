from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from PIL import Image
import os

class PDFConverter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.selected_files = []

        self.label = Label(text="No images selected", size_hint=(1, 0.1))
        self.add_widget(self.label)

        btn_select = Button(text="Select Images", size_hint=(1, 0.2), background_color=(1, 0.5, 0, 1))
        btn_select.bind(on_press=self.select_images)
        self.add_widget(btn_select)

        btn_convert = Button(text="Convert to PDF", size_hint=(1, 0.2), background_color=(0, 0.6, 1, 1))
        btn_convert.bind(on_press=self.convert_to_pdf)
        self.add_widget(btn_convert)

    def select_images(self, instance):
        filechooser = FileChooserListView(multiselect=True, filters=['*.png', '*.jpg', '*.jpeg'])
        popup = Popup(title="Select Images", content=filechooser, size_hint=(0.9, 0.9))

        def on_selection(instance, selection):
            if selection:
                self.selected_files = selection
                self.label.text = f"{len(selection)} images selected"
                popup.dismiss()

        filechooser.bind(selection=on_selection)
        popup.open()


    def convert_to_pdf(self, instance):
        if not self.selected_files:
            self.label.text = "No images selected!"
            return

        images = [Image.open(img).convert("RGB") for img in self.selected_files]
        save_path = os.path.join(os.getcwd(), "output.pdf")
        images[0].save(save_path, save_all=True, append_images=images[1:])
        self.label.text = f"PDF saved: {save_path}"

class ImageToPDFApp(App):
    def build(self):
        return PDFConverter()

if __name__ == '__main__':
    ImageToPDFApp().run()
