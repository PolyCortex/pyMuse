from kivy.app import App
#kivy.require("1.9.1")

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

class GridAlpha(GridLayout):
    def __init__(self, **kwargs):
        super(GridAlpha, self).__init__(**kwargs)

        def ColumnCounter(array = []):

            initialLenght = len(array)
            counter = 1
            print initialLenght
            return;


        p300AlphaNumbers = ["A", "B","C", "D", "E", "F","G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                            "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


        ColumnCounter(p300AlphaNumbers)



        self.cols = 6

        for elements in p300AlphaNumbers:
            self.add_widget(Label(text=elements,font_size = '40sp'))




class SimpleKivy(App):
    def build(self):
        return GridAlpha()

if __name__ == "__main__":
    SimpleKivy().run()




