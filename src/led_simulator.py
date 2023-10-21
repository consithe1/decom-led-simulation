from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image
import math


def calculate_distance(coords):
    x1, y1, x2, y2 = coords
    return int(math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)))


class LEDSimulator(Tk):
    def __init__(self):
        super().__init__()

        self.px_to_mm_val = 1
        self.tk_image = None
        self.current_line = []
        self.led_strips = []
        self.leds = []

        self.image_file = None
        self.window_canvas = None
        self.window_background = None
        self.id_shape = None
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        self.referential = {"last_id": None, "origin_x": None, "origin_y": None, "dest_x": None, "dest_y": None}
        self.referential_line = None
        self.measuring = False

        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.title("LED Simulator")

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # MENU
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)
        self.menu_files = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.menu_files)
        self.menu_files.add_command(label='Open image', command=self.open_image)

        # FRAME DESCRIPTION
        self.frame_description = Frame(self, bg="cyan", highlightbackground="black", highlightthickness=1)
        self.frame_description.columnconfigure(0, weight=1)
        self.label_description = Label(self.frame_description, text="Description du projet")
        self.label_description.pack(expand=True, fill=BOTH)

        self.frame_description.grid(sticky="nsew", padx=5, pady=5)

        # FRAME IMAGE/CANVAS
        self.frame_image = Frame(self, bg="lavender")

        self.image_canvas = Canvas(self.frame_image, width=self.width, height=self.height)
        self.image_canvas.pack(expand=True, fill=BOTH)
        self.image_canvas.bind("<Motion>", self.update_position)
        self.image_canvas.bind("<Button-1>", self.button_1_pressed)
        self.image_canvas.bind("<B1-Motion>", self.add_line)
        self.image_canvas.bind("<ButtonRelease-1>", self.button_1_released)
        self.frame_image.grid(row=1, sticky="nsew")
        self.label_measure = Label(self.frame_image, text="")

        # FRAME OPTIONS
        self.frame_options = Frame(self, bg="forestgreen")

        # FRAME MODE
        self.mode = StringVar()
        self.frame_mode = Frame(self.frame_options)
        Label(self.frame_mode, text="Mode selection:").grid(row=0, column=0)
        Radiobutton(self.frame_mode, text="Enable measuring", variable=self.mode, value="measuring",
                    command=self.update_mode).grid(row=0, column=1)
        Radiobutton(self.frame_mode, text="Enable drawing", variable=self.mode, value="drawing",
                    command=self.update_mode).grid(row=0, column=2)
        self.mode.set("measuring")

        self.frame_mode.grid(row=0, columnspan=4, sticky="news")

        # FRAME MEASURING
        self.frame_measuring = Frame(self.frame_options, highlightbackground="black", highlightthickness=1)
        Label(self.frame_measuring, text="Dimensions").grid(row=0, columnspan=3, sticky='ew')
        self.distance_pixel_var = StringVar()
        self.distance_pixel_var.set(str(0))
        self.distance_pixel_label = Label(self.frame_measuring, textvariable=self.distance_pixel_var)
        self.distance_pixel_label.grid(row=1, column=0, sticky='ew')
        Label(self.frame_measuring, text="px =").grid(row=1, column=1, sticky='ew')
        self.distance_mm_var = StringVar()
        self.distance_mm_var.set(str(1000))
        self.distance_mm_entry = Entry(self.frame_measuring, textvariable=self.distance_mm_var)
        self.distance_mm_entry.grid(row=1, column=2, sticky='ew')
        Label(self.frame_measuring, text="mm").grid(row=1, column=3, sticky='ew')
        Button(self.frame_measuring, text='Clear', command=self.clear_canvas).grid(row=2, sticky="ew", columnspan=4)
        self.px_to_mm_label = Label(self.frame_measuring, text="Equivalent: None")
        self.px_to_mm_label.grid(row=3, columnspan=4, sticky="ew")
        self.frame_measuring.grid(row=1, column=0, sticky="news", padx=5)

        # FRAME DRAWING
        self.frame_drawing = Frame(self.frame_options, highlightbackground="black", highlightthickness=1)
        Label(self.frame_drawing, text="LED Drawing").grid(row=0, sticky="ew", columnspan=2)

        self.led_densities = [30, 60, 144]
        self.led_density_var = StringVar()
        self.led_density_var.set(str(self.led_densities[0]))
        for index, shape in enumerate(self.led_densities):
            Radiobutton(self.frame_drawing, text=f"{shape} LEDs/m", variable=self.led_density_var, value=shape,
                        command=self.update_density_value).grid(row=index + 2, column=0, sticky="w")
        Button(self.frame_drawing, text="Clear", command=self.clear_canvas).grid(row=2, column=1, sticky="ew")
        Button(self.frame_drawing, text="Undo", command=self.undo_last_draw).grid(row=3, column=1, sticky="ew")
        Button(self.frame_drawing, text="Generate LED strip", command=self.generate_led_strip).grid(row=4, column=1, sticky="ew")
        Button(self.frame_drawing, text="Save LED strip").grid(row=5, column=1, sticky="ew")  # TODO: add command

        self.frame_drawing.grid(row=1, column=1, sticky="news", padx=5)

        # FRAME SEQUENCE TO RUN
        self.frame_sequence = Frame(self.frame_options, highlightbackground="black", highlightthickness=1)
        Label(self.frame_sequence, text="Sequence Options").grid(row=1, column=2, sticky="ew")
        # cursor led size
        # sequence selection
        # run button
        self.frame_sequence.grid(row=1, column=2, sticky="news", padx=5)

        # Position x-y
        self.frame_cursor_position = Frame(self.frame_options)
        self.cursor_pos_var = StringVar()
        self.cursor_pos_var.set("Position: init")
        self.cursor_pos_label = Label(self.frame_cursor_position, textvariable=self.cursor_pos_var, anchor="e",
                                      relief=SUNKEN)
        self.cursor_pos_label.pack()
        self.frame_cursor_position.grid(row=1, column=3, sticky="news", padx=5)

        self.frame_options.grid(row=2, columnspan=1, sticky="news", padx=5, pady=5)
        self.update_mode()

    def update_mode(self):
        if self.mode.get() == "drawing":
            for child in self.frame_measuring.winfo_children():
                child.configure(state='disable')
            for child in self.frame_drawing.winfo_children():
                child.configure(state='normal')

        if self.mode.get() == "measuring":
            for child in self.frame_measuring.winfo_children():
                child.configure(state='normal')
            for child in self.frame_drawing.winfo_children():
                child.configure(state='disable')

    def button_1_pressed(self, event):
        if self.mode.get() == "drawing":
            self.lastx, self.lasty = event.x, event.y

        if self.mode.get() == "measuring" and not self.measuring:
            self.referential['origin_x'] = event.x
            self.referential['origin_y'] = event.y
            self.measuring = True
        self.update_position(event)

    def add_line(self, event):
        if self.mode.get() == "drawing":
            line_id = self.image_canvas.create_line(self.lastx, self.lasty, event.x, event.y, fill="red", width=2,
                                                    tags="drawing")
            self.current_line.append([line_id, self.image_canvas.coords(line_id)])
            self.button_1_pressed(event)

        if self.mode.get() == "measuring":
            if self.referential['last_id'] is not None:
                self.clear_canvas(self.referential['last_id'])
            line_id = self.image_canvas.create_line(self.referential['origin_x'], self.referential['origin_y'], event.x,
                                                    event.y, fill="blue", dash=(10, 5), width=2, tags='measuring',
                                                    arrow=BOTH)
            self.referential['last_id'] = line_id
            self.referential_line = [line_id, self.image_canvas.coords(line_id)]
            self.update_referential(calculate_distance(self.image_canvas.coords(line_id)))

    def open_image(self):
        self.clear_canvas()
        self.image_file = filedialog.askopenfilename(title="Open file",
                                                     filetypes=[('JPEG Files', '.jpg'), ('PNG Files', '.png')])
        image = Image.open(self.image_file)
        image_resized = image.resize((self.width, self.height))

        self.tk_image = ImageTk.PhotoImage(image_resized)
        self.image_canvas.create_image(0, 0, image=self.tk_image, anchor='nw')

    def update_position(self, event=None):
        self.cursor_pos_var.set(f"Position: ({event.x}, {event.y})")
        self.cursor_pos_label.update()

    def update_referential(self, length):
        self.distance_pixel_var.set(f"{length}")
        self.distance_pixel_label.update()

    def undo_last_draw(self):
        if len(self.led_strips) != 0:
            to_delete = self.led_strips.pop()
            for id_line, _ in to_delete:
                self.image_canvas.delete(id_line)

    def clear_canvas(self, id_line=None):
        if self.mode.get() == 'drawing':

            while len(self.led_strips) != 0:
                self.undo_last_draw()
            self.led_strips = []
            self.update_description()

        if self.mode.get() == 'measuring':
            if self.referential_line is not None:
                self.image_canvas.delete(self.referential_line[0])
            self.referential_line = None
            self.label_measure.destroy()

    def update_density_value(self):
        self.update_description()

    def button_1_released(self, event):
        if self.mode.get() == "drawing":
            led_strip = self.current_line.copy()
            self.led_strips.append(led_strip)
            self.current_line = []
            self.update_description()

        if self.mode.get() == "measuring":
            self.referential['dest_x'] = event.x
            self.referential['dest_y'] = event.y
            self.measuring = False
            self.validate_equivalence_px_to_mm()

    def place_label_measure(self):
        self.label_measure = Label(self.frame_image, text=f"{self.distance_mm_var.get()} mm")
        self.label_measure.place(x=(self.referential_line[1][0] + self.referential_line[1][2]) / 2 - 30,
                                 y=(self.referential_line[1][1] + self.referential_line[1][3]) / 2 + 10)

    def validate_equivalence_px_to_mm(self):
        self.px_to_mm_val = 1
        if self.referential_line is not None:
            self.px_to_mm_val = int(self.distance_mm_var.get()) / int(self.distance_pixel_var.get())
        self.px_to_mm_label.config(text=f"Equivalent: {1} px = {self.px_to_mm_val:.2f} mm")
        self.place_label_measure()

    def update_description(self):
        total_length_px = 0
        for strip in self.led_strips:
            for strip_id, coords in strip:
                total_length_px += calculate_distance(coords)
        total_length_mm = int(total_length_px * self.px_to_mm_val)

        number_leds = int(int(self.led_density_var.get()) * total_length_mm / 1000)

        self.label_description.config(text=f"Total length: {total_length_mm} mm / # of LEDs: {number_leds}")

    def generate_led_strip(self):
        self.update_description()

        # generate points on the led_strip lines

