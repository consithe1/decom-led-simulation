from tkinter import *
from tkinter import filedialog
import math

from PIL import ImageTk, Image

MASK_B1 = 0x0100


class LEDSimulator(Tk):
    def __init__(self, width=800, height=400):
        super().__init__()

        self.left_click_pressed = False
        self.tk_image = None
        self.current_line = []
        self.led_lines = []
        self.drawing_ids = []

        self.drawing_action = True
        self.measuring_action = False

        self.image_file = None
        self.window_canvas = None
        self.window_background = None
        self.id_shape = None
        self.width = width
        self.height = height

        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.title("LED Simulator")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # MENU
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)
        self.menu_files = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.menu_files)
        self.menu_files.add_command(label='Open image', command=self.open_image)

        # FRAME DESCRIPTION
        self.frame_description = Frame(self, bg="cyan", width=50, height=150)
        Label(self.frame_description, text="Description du projet").pack()

        self.frame_description.grid(sticky="nsew")

        # FRAME IMAGE/CANVAS
        self.frame_image = Frame(self, bg="lavender", width=50, height=150)

        self.image_canvas = Canvas(self.frame_image, width=self.width, height=self.height)
        self.image_canvas.pack(expand=True, fill=BOTH)
        self.image_canvas.bind("<Motion>", self.update_position)
        self.image_canvas.bind("<Button-1>", self.save_posn)
        self.image_canvas.bind("<B1-Motion>", self.add_line)
        self.image_canvas.bind("<ButtonRelease-1>", self.add_full_line)
        self.frame_image.grid(row=1, sticky="nsew")

        # FRAME OPTIONS
        self.frame_options = Frame(self, bg="forestgreen", width=50, height=150)

        # FRAME DIMENSIONS
        self.frame_dimensions = Frame(self.frame_options)
        Label(self.frame_dimensions, text="Dimensions").grid(row=0, column=0)
        self.frame_dimensions.grid(row=0, column=0, sticky="news")

        # FRAME LED STRIPS DRAWING
        self.frame_drawing = Frame(self.frame_options, highlightbackground="black", highlightthickness=1)
        Label(self.frame_drawing, text="LED positions").grid(row=0, sticky="ew", columnspan=2)
        self.led_densities = [30, 60, 144]
        self.led_density = StringVar()
        self.led_density.set(str(self.led_densities[0]))
        for index, shape in enumerate(self.led_densities):
            Radiobutton(self.frame_drawing, text=f"{shape} LEDs/m", variable=self.led_density, value=shape,
                        command=self.update_density_value).grid(row=index + 1, column=0, sticky="w")
        Button(self.frame_drawing, text="Clear", command=self.clear_canvas).grid(row=1, column=1, sticky="ew")
        Button(self.frame_drawing, text="Undo", command=self.undo_last_draw).grid(row=2, column=1, sticky="ew")
        Button(self.frame_drawing, text="Generate LED strip").grid(row=3, column=1, sticky="ew")  # TODO: add command
        Button(self.frame_drawing, text="Save LED strip").grid(row=4, column=1, sticky="ew")  # TODO: add command

        self.frame_drawing.grid(row=0, column=1, sticky="news")

        # FRAME SEQUENCE TO RUN
        self.frame_sequence = Frame(self.frame_options, highlightbackground="black", highlightthickness=1)
        Label(self.frame_sequence, text="Sequence Options").grid(row=0, sticky="ew")
        # cursor led size
        # sequence selection
        # run button

        # Position x-y
        self.frame_cursor_position = Frame(self.frame_options)
        self.cursor_pos_var = StringVar()
        self.cursor_pos_var.set("Position: init")
        self.cursor_pos_label = Label(self.frame_cursor_position, textvariable=self.cursor_pos_var, anchor="e",
                                      relief=SUNKEN)
        self.cursor_pos_label.pack()
        self.frame_cursor_position.grid(row=0, column=3, sticky="news")

        self.frame_options.grid(row=2, sticky="ew", padx=5, pady=5)

    def save_posn(self, event):
        self.lastx, self.lasty = event.x, event.y
        self.update_position(event)

    def add_line(self, event):
        line_id = self.image_canvas.create_line(self.lastx, self.lasty, event.x, event.y, fill="red", width=2,
                                                tags="drawing")
        self.current_line.append([line_id, self.image_canvas.coords(line_id)])
        self.save_posn(event)

    def open_image(self):
        self.image_file = filedialog.askopenfilename(title="Open file",
                                                     filetypes=[('JPEG Files', '.jpg'), ('PNG Files', '.png')])
        image = Image.open(self.image_file)
        image_resized = image.resize((self.width, self.height))

        self.tk_image = ImageTk.PhotoImage(image_resized)
        self.image_canvas.create_image(0, 0, image=self.tk_image, anchor='nw')

    def update_position(self, event=None):
        self.cursor_pos_var.set(f"Position: x - {event.x}, y - {event.y}")
        self.cursor_pos_label.update()

    def update_description(self):
        pass

    def undo_last_draw(self):
        if len(self.led_lines) != 0:
            to_delete = self.led_lines.pop()
            for id_line, _ in to_delete:
                self.image_canvas.delete(id_line)

    def clear_canvas(self, tag="drawing"):
        self.image_canvas.delete(tag)
        self.led_lines = []

    def update_density_value(self):
        print(f"LED Density: {self.led_density.get()} LEDs/m")

    def add_full_line(self, event):
        self.led_lines.append(self.current_line)
        print("Line length:", self.calculate_line_length(self.current_line), "pixels")
        self.current_line = []

    def calculate_line_length(self, full_line):
        d_total = 0
        for id_line, line in full_line:
            x1, y1, x2, y2 = line
            d_total += math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        return int(d_total)
