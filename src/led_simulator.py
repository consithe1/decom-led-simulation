from tkinter import *
from tkinter import filedialog
from src.rgb_leds.referential import Referential
from src.rgb_leds.LEDStrip import LEDStrip

from PIL import ImageTk, Image
import math


def calculate_distance(coords):
    x1, y1, x2, y2 = coords
    return int(math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)))


def generate_path_between_coordinates(src_coords, dest_coords):
    x_src, y_src = src_coords
    x_dest, y_dest = dest_coords
    path = []

    if x_dest - x_src < 0:
        if y_dest - y_src < 0:
            for x in range(x_src, x_dest, -1):
                for y in range(y_src, y_dest, -1):
                    path.append((x, y))
        elif y_dest - y_src == 0:
            for x in range(x_src, x_dest, -1):
                path.append((x, y_src))
        else:
            for x in range(x_src, x_dest, -1):
                for y in range(y_src, y_dest, 1):
                    path.append((x, y))
    elif x_dest - x_src == 0:
        if y_dest - y_src < 0:
            for y in range(y_src, y_dest, -1):
                path.append((x_src, y))
        elif y_dest - y_src > 0:
            for y in range(y_src, y_dest, 1):
                path.append((x_src, y))
    else:
        if y_dest - y_src < 0:
            for x in range(x_src, x_dest, 1):
                for y in range(y_src, y_dest, -1):
                    path.append((x, y))
        elif y_dest - y_src == 0:
            for x in range(x_src, x_dest, 1):
                path.append((x, y_src))
        else:
            for x in range(x_src, x_dest, 1):
                for y in range(y_src, y_dest, 1):
                    path.append((x, y))

    return path


class LEDSimulator(Tk):
    def __init__(self):
        super().__init__()

        self.last_x = None
        self.last_y = None
        self.referential = Referential()

        self.tk_image = None
        self.current_drawing_strip = []

        self.led_strips: list[LEDStrip] = []

        self.image_file = None
        self.window_canvas = None
        self.window_background = None
        self.id_shape = None
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

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
        self.label_description = Label(self.frame_description, text="Project description")
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
        self.label_ref = Label(self.frame_image, text=f"{self.referential.get_dist_mm_src_to_dest()} mm")

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

        # FRAME REFERENTIAL
        self.frame_measuring = Frame(self.frame_options, highlightbackground="black", highlightthickness=1)
        Label(self.frame_measuring, text="Referential").grid(row=0, columnspan=3, sticky='ew')
        self.distance_pixel_var = StringVar()
        self.distance_pixel_var.set(str(0))
        self.distance_pixel_label = Label(self.frame_measuring, textvariable=self.distance_pixel_var)
        self.distance_pixel_label.grid(row=1, column=0, sticky='ew')
        Label(self.frame_measuring, text="px =").grid(row=1, column=1, sticky='ew')
        self.distance_mm_var = IntVar(value=1000)
        self.distance_mm_var.trace_add('write', self.update_label_ref_callback)
        self.distance_mm_entry = Entry(self.frame_measuring, textvariable=self.distance_mm_var)
        self.distance_mm_entry.grid(row=1, column=2, sticky='ew')
        Label(self.frame_measuring, text="mm").grid(row=1, column=3, sticky='ew')
        Button(self.frame_measuring, text='Clear', command=self.clear_canvas).grid(row=3, sticky="ew", columnspan=4)
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
        Button(self.frame_drawing, text="Generate LED strip", command=self.generate_led_strip).grid(row=4, column=1,
                                                                                                    sticky="ew")
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
            self.last_x, self.last_y = event.x, event.y

        if self.mode.get() == "measuring" and not self.measuring:
            self.referential.set_origin(event.x, event.y)
            self.measuring = True
        self.update_position(event)

    def add_line(self, event):
        # TODO treatment to avoid accumulation of points at the same place
        if self.mode.get() == "drawing":
            line_id = self.image_canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill="red", width=1,
                                                    tags="drawing")
            self.current_drawing_strip.append([line_id, [self.last_x, self.last_y, event.x, event.y]])
            self.button_1_pressed(event)

        if self.mode.get() == "measuring":
            if self.referential.get_id_line_canvas() is not None:
                self.clear_canvas(self.referential.get_id_line_canvas())
            self.referential.update_referential(event.x, event.y, self.distance_mm_var.get())
            self.referential.set_id_line_canvas(
                self.image_canvas.create_line(self.referential.get_x_src(), self.referential.get_y_src(),
                                              self.referential.get_x_dest(),
                                              self.referential.get_y_dest(), fill="blue", dash=(10, 5), width=2,
                                              tags='measuring',
                                              arrow=BOTH))

            # update the ref label
            self.update_label_ref()
            self.update_label_ref_ratio()

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

    def undo_last_draw(self, id_obj):
        self.image_canvas.delete(id_obj)

    def clear_canvas(self, id_line=None):
        if self.mode.get() == 'drawing':
            for led_strip in self.led_strips:
                [self.undo_last_draw(id_obj) for id_obj in led_strip.delete_object()]

            self.led_strips = []

        if self.mode.get() == 'measuring':
            if self.referential.exists():
                self.image_canvas.delete(self.referential.remove_from_canvas())
                self.remove_label_ref()

    def update_density_value(self):
        self.update_description()

    def button_1_released(self, event):
        if self.mode.get() == "drawing":
            self.led_strips.append(LEDStrip(self.current_drawing_strip.copy()))
            self.current_drawing_strip = []

        if self.mode.get() == "measuring":
            self.add_line(event)
            self.measuring = False

    def remove_label_ref(self):
        self.label_ref.destroy()

    def update_label_ref(self):
        self.remove_label_ref()
        self.label_ref = Label(self.frame_image, text=f"{self.referential.get_dist_mm_src_to_dest()} mm")
        self.label_ref.place(x=(self.referential.get_x_src() + self.referential.get_x_dest()) / 2 - 30,
                             y=(self.referential.get_y_src() + self.referential.get_y_dest()) / 2 + 10)

    def update_label_ref_ratio(self):
        self.px_to_mm_label.config(text=f"1 px = {self.referential.get_ratio_px_to_mm()} mm")

    def update_label_ref_callback(self, var, index, mode):
        try:
            var = self.distance_mm_var.get()
        except TclError:
            var = 0
        self.referential.set_dist_mm_src_to_dest(var)
        self.update_label_ref_ratio()
        self.update_label_ref()

    def update_description(self):
        # TODO description not properly updated
        pass

    def generate_led_strip(self):
        # TODO
        pass
