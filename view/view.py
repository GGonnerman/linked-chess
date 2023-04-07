import tkinter
from view.constants import SIDE_LENGTH, BOX_LENGTH
from view.box import Box

class View():

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.resizable(0, 0)
        self.canvas = tkinter.Canvas(
            self.root,
            width=SIDE_LENGTH,
            # Double, then one row of 'boxes' as padding between
            height=SIDE_LENGTH*2+BOX_LENGTH,
            background='#AAAAAA'
        )
        self.canvas.grid(row=0, column=0)
        self.upper_boxes = []
        self.lower_boxes = []
        # Create the upper gameboard
        for row in range(8):
            upper_row_of_boxes = []
            lower_row_of_boxes = []
            for column in range(8):
                upper_row_of_boxes.append(Box(row, column, self.canvas))
                lower_row_of_boxes.append(Box(row, column, self.canvas, offset_y=BOX_LENGTH*9))
            self.upper_boxes.append(upper_row_of_boxes)
            self.lower_boxes.append(lower_row_of_boxes)
    
    def get_root(self):
        return self.root
    
    def get_canvas(self):
        return self.canvas
    
    def bind_mouse_click(self, click_event):
        self.bind_button_event("<Button-1>", click_event)

    def bind_escape(self, escape_event):
        self.bind_button_event("<Escape>", escape_event)
    
    def bind_button_event(self, button, event):
        self.canvas.focus_set()
        self.canvas.bind(button, event)
