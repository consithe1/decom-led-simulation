from tkinter import *
from tkinter import filedialog
from src.rgb_leds.referential import Referential
from src.rgb_leds.LEDStrip import LEDStrip

from PIL import ImageTk, Image


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
        self.led_density_var = IntVar()
        self.led_density_var.set(self.led_densities[0])
        for index, d in enumerate(self.led_densities):
            Radiobutton(self.frame_drawing, text=f"{d} LEDs/m", variable=self.led_density_var, value=d,
                        command=self.update_density_value).grid(row=index + 2, column=0, sticky="w")
        Button(self.frame_drawing, text="Clear", command=self.clear_canvas).grid(row=2, column=1, sticky="ew")
        Button(self.frame_drawing, text="Undo", command=self.undo_last_draw).grid(row=3, column=1, sticky="ew")
        Button(self.frame_drawing, text="Generate LED strip", command=self.generate_led_strips).grid(row=4, column=1,
                                                                                                     sticky="ew")
        Button(self.frame_drawing, text="Save LED strip").grid(row=5, column=1, sticky="ew")  # TODO: add command

        self.frame_drawing.grid(row=1, column=1, sticky="news", padx=5)

        # FRAME SEQUENCE TO RUN
        self.frame_sequence = Frame(self.frame_options, highlightbackground="black", highlightthickness=1)
        Label(self.frame_sequence, text="Sequence Options").grid(row=0, sticky="ew")
        # cursor led size
        self.led_size_px_val = IntVar()
        self.led_size_px_val.set(2)
        Scale(self.frame_sequence, label="LED Size (px)", command=self.update_leds, from_=2, to=10, orient=HORIZONTAL, resolution=1, variable=self.led_size_px_val).grid(row=1, sticky="ew")
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

    def update_leds(self, new_value):
        self.generate_led_strips()

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

    def add_line(self, event):
        # TODO treatment to avoid accumulation of points at the same place
        if self.mode.get() == "drawing":
            line_id = self.image_canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill="red", width=1,
                                                    tags="drawing", smooth=True)
            self.current_drawing_strip.append([line_id, [self.last_x, self.last_y, event.x, event.y]])
            self.button_1_pressed(event)

        if self.mode.get() == "measuring":
            if self.referential.get_id_line_canvas() is not None:
                self.remove_obj_from_canvas(self.referential.get_id_line_canvas())
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

    def remove_obj_from_canvas(self, id_obj):
        self.image_canvas.delete(id_obj)

    def undo_last_draw(self):
        if len(self.led_strips) != 0:
            obj_to_del = self.led_strips.pop()
            ids_to_del = obj_to_del.delete_object()
            [self.remove_obj_from_canvas(id_del) for id_del in ids_to_del]

    def remove_objs_from_canvas(self, list_ids: list[int]):
        [self.remove_obj_from_canvas(id_obj) for id_obj in list_ids]

    def clear_canvas(self):
        if self.mode.get() == 'drawing':
            for led_strip in self.led_strips:
                [self.remove_obj_from_canvas(id_obj) for id_obj in led_strip.delete_object()]

            self.led_strips = []

        elif self.mode.get() == 'measuring':
            if self.referential.exists():
                self.image_canvas.delete(self.referential.remove_from_canvas())
                self.remove_label_ref()

    def update_density_value(self):
        self.update_leds(2)

    def draw_spline_line(self, coords):
        new_ids = []
        for x1, y1, x2, y2 in coords:
            new_ids.append([self.image_canvas.create_line(x1, y1, x2, y2, fill="green", width=2), [x1, y1, x2, y2]])
        return new_ids

    def button_1_released(self, event):
        self.add_line(event)
        if self.mode.get() == "measuring":
            self.measuring = False

        elif self.mode.get() == "drawing":
            self.led_strips.append(LEDStrip(self.current_drawing_strip.copy()))
            self.current_drawing_strip = []

    def button_1_pressed(self, event):
        if self.mode.get() == "drawing":
            self.last_x, self.last_y = event.x, event.y

        elif self.mode.get() == "measuring" and not self.measuring:
            self.referential.set_origin(event.x, event.y)
            self.measuring = True
        self.update_position(event)

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

    def update_all_variables_and_fields(self):
        # TODO call every update function
        pass

    def generate_led_strips(self):

        prev_strip_index, prev_led_index, prev_led_id = -1, -1, None

        for i in range(len(self.led_strips)):
            # remove previous leds from canvas, LEDStrip list
            self.remove_objs_from_canvas(self.led_strips[i].remove_leds())
            # calculate new led positions based on LED density and LED size
            self.led_strips[i].calculate_led_positions(self.referential.get_ratio_px_to_mm(), self.led_density_var.get(), self.led_size_px_val.get())

            # add leds to canvas
            for j in range(len(self.led_strips[i].get_list_leds())):
                # calculate rectangle object associated to LED
                # depends on the LED density and the LED size in px
                x0, y0, x1, y1 = self.led_strips[i].get_list_leds()[j].get_rect_coordinates()
                # draw the LED rectangles on canvas
                new_id_led = self.image_canvas.create_rectangle(x0, y0, x1, y1, fill="pink")

                # exchange information between LEDs and strips
                self.led_strips[i].add_id_canvas_to_led(j, new_id_led)
                if prev_led_id is not None:
                    self.led_strips[i].add_prev_id_canvas_to_led(j, prev_led_id)
                    self.led_strips[prev_strip_index].add_next_id_canvas_to_led(prev_led_index, new_id_led)

                prev_strip_index, prev_led_index, prev_led_id = i, j, new_id_led

            print(f"Number of LEDs in this strip: {self.led_strips[i].calculate_number_leds()}")
