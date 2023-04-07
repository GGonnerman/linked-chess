import tkinter
from color import Color
from view.constants import BOX_LENGTH

# A box is each of the 'square' on the chess board
# It contains a color that is used for highlighting and general background stuff
# Additionally, it holds a row and column used for placing itself
class Box():
    def __init__(self, row, column, canvas, offset_x=0, offset_y=0):
        self.canvas = canvas
        self.row = row
        self.column = column
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.color = '#F7ECCA' if (row + column) % 2 == 0 else '#66442E'
        self.id = canvas.create_rectangle(
            column * BOX_LENGTH + offset_x, # Start_x
            row * BOX_LENGTH + offset_y, # Start_y
            (column + 1) * BOX_LENGTH + offset_x, # End_x
            (row + 1) * BOX_LENGTH + offset_y, # End_y
            fill=self.color
        )
        self.photo_image_name = None
        self.photo_id = None

    def clear_highlighting(self):
        self.canvas.itemconfig(self.id, {'fill': self.color})
    
    def select(self):
        color = '#CAEDF7' if self.color == '#F7ECCA' else '#3E7989'
        if True: #self.movement_hints:
            config = {'fill': color}
        else:
            config = {'fill': self.color}
        self.canvas.itemconfig(self.id, config)
    
    def issue(self):
        color = '#F77C7C' if self.color == '#F7ECCA' else '#F74A4A'
        if True: #self.movement_hints:
            config = {'fill': color}
        else:
            config = {'fill': self.color}
        self.canvas.itemconfig(self.id, config)

    def highlight(self):
        self.highlighted = True
        color = '#C2F7AD' if self.color == '#F7ECCA' else '#51662E'
        if True: #self.movement_hints:
            config = {'fill': color}
        else:
            config = {'fill': self.color}
        self.canvas.itemconfig(self.id, config)
    
    def get_center_coords(self):
        return [
            self.column * BOX_LENGTH + (BOX_LENGTH / 2) + self.offset_x,
            self.row * BOX_LENGTH + (BOX_LENGTH / 2) + self.offset_y,
        ]
    
    def display_image(self, file_name):
        self.photo_image_name = file_name
        self._photo_image = tkinter.PhotoImage(file="media/" + self.photo_image_name + ".png")
        self.photo_id = self.canvas.create_image(self.get_center_coords(), image=self._photo_image)

    
    def clear_image(self):
        self.photo_image_name = None
        self.canvas.delete(self.photo_id)
        self.photo_id = None
