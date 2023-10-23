from tkinter import *
from tkinter import filedialog
from src.rgb_leds.led import LED
from src.utils.parameters import Parameters
from src.utils.constants import *
from src.utils.file_utils import FileUtils
from PIL import ImageTk, Image
import logging


class LEDSimulator(Tk):
    def __init__(self):
        self.id_image_canvas = None
        logging.debug("Creating main frame")
        super().__init__()

        self.last_x = None
        self.last_y = None

        self.current_drawing_strip = []

        # to read from simulation file
        self.parameters = Parameters()

        self.parameters["width"] = self.winfo_screenwidth()
        self.parameters["height"] = self.winfo_screenheight()

        self.measuring = False
        self.tk_image = None

        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.title("LED Simulator")

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        """
        MENU BAR
        """
        logging.debug("Creating menu bar")
        self.option_add('*tearOff', FALSE)
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)

        self.menu_led_display = Menu(self.menu_bar)

        self.menu_led_display.add_command(label='Open LED Display', command=self.open_existing_simulation)
        self.menu_led_display.add_command(label='Save LED Display', command=self.save_simulation_to_file)
        self.menu_led_display.add_command(label='Exit', command=self.quit)
        self.menu_bar.add_cascade(label="LED Display", menu=self.menu_led_display)

        self.menu_background = Menu(self.menu_bar)
        self.menu_background.add_command(label='Add Image to background', command=self.open_image_with_ask_dialog)
        self.menu_bar.add_cascade(label="Background", menu=self.menu_background)

        # FRAME DESCRIPTION
        self.frame_description = Frame(self, bg="cyan", highlightbackground="black", highlightthickness=1)
        self.frame_description.columnconfigure(0, weight=1)
        self.label_description = Label(self.frame_description, text="Project description")
        self.label_description.pack(expand=True, fill=BOTH)

        self.frame_description.grid(sticky="nsew", padx=5, pady=5)

        # FRAME IMAGE/CANVAS
        logging.debug("Creating drawing canvas")
        self.frame_image = Frame(self, bg="lavender")

        self.image_canvas = Canvas(self.frame_image, width=self.parameters["width"],
                                   height=self.parameters["height"])
        self.image_canvas.pack(expand=True, fill=BOTH)
        self.image_canvas.bind("<Motion>", self.update_position)
        self.image_canvas.bind("<Button-1>", self.button_1_pressed)
        self.image_canvas.bind("<B1-Motion>", self.add_line)
        self.image_canvas.bind("<ButtonRelease-1>", self.button_1_released)
        self.frame_image.grid(row=1, sticky="nsew")
        self.label_ref = Label(self.frame_image,
                               text=f'{self.parameters["referential"]["dist_mm_src_to_dest"]} mm')

        # FRAME OPTIONS
        logging.debug("Creating Options frame")
        self.frame_options = Frame(self, bg="forestgreen")

        # FRAME MODE
        self.mode = StringVar()
        self.frame_mode = Frame(self.frame_options)
        Label(self.frame_mode, text="Mode selection:").grid(row=0, column=0)
        Radiobutton(self.frame_mode, text="Enable measuring", variable=self.mode, value=MEASURING,
                    command=self.update_all_variables_and_fields).grid(row=0, column=1)
        Radiobutton(self.frame_mode, text="Enable drawing", variable=self.mode, value=DRAWING,
                    command=self.update_all_variables_and_fields).grid(row=0, column=2)
        self.mode.set(MEASURING)

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

        self.led_density_var = IntVar()
        self.led_density_var.set(LED_DENSITIES[0])
        for index, d in enumerate(LED_DENSITIES):
            Radiobutton(self.frame_drawing, text=f"{d} LEDs/m", variable=self.led_density_var, value=d,
                        command=self.update_all_variables_and_fields).grid(row=index + 2, column=0, sticky="w")
        Button(self.frame_drawing, text="Clear", command=self.clear_canvas).grid(row=2, column=1, sticky="ew")
        Button(self.frame_drawing, text="Undo", command=self.undo_last_draw).grid(row=3, column=1, sticky="ew")
        Button(self.frame_drawing, text="Generate LED strip", command=self.update_all_variables_and_fields).grid(row=4,
                                                                                                                 column=1,
                                                                                                                 sticky="ew")
        Button(self.frame_drawing, text="Save LED strip").grid(row=5, column=1, sticky="ew")  # TODO: add command

        self.frame_drawing.grid(row=1, column=1, sticky="news", padx=5)

        # FRAME SEQUENCE TO RUN
        self.frame_sequence = Frame(self.frame_options, highlightbackground="black", highlightthickness=1)
        Label(self.frame_sequence, text="Sequence Options").grid(row=0, sticky="ew")
        # cursor led size
        self.led_size_px_var = IntVar()
        self.led_size_px_var.set(2)
        Scale(self.frame_sequence, label="LED Size (px)", command=self.update_all_variables_and_fields, from_=2, to=10,
              orient=HORIZONTAL,
              resolution=1, variable=self.led_size_px_var).grid(row=1, sticky="ew")
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

    """
    DRAWING FUNCTIONS
    """

    def open_image_with_ask_dialog(self):
        self.parameters["image_src_path"] = filedialog.askopenfilename(title="Open file",
                                                                       filetypes=[('JPEG Files', '*.jpg'),
                                                                                  ('PNG Files', '*.png')],
                                                                       defaultextension='.jpg', initialdir=DIR_IMAGE_DEFAULT)
        self.open_image(self.parameters["image_src_path"])
        self.draw_referential_line()
        self.draw_led_lines()
        self.draw_led_strips()

    def open_image(self, image_path=None):
        logging.debug(f"Opening image file at {image_path}")
        if image_path is not None:
            image = Image.open(image_path)
            image_resized = image.resize((self.parameters["width"], self.parameters["height"]))

            self.tk_image = ImageTk.PhotoImage(image_resized)
            self.id_image_canvas = self.image_canvas.create_image(0, 0, image=self.tk_image, anchor='nw')

    def open_existing_simulation(self):
        # TODO if new simu is opened while another one has been opened, LEDs are overlapping
        dict_simu = FileUtils.read_simulation_from_file(
            filedialog.askopenfilename(
                title="Open Simulation File", filetypes=[('Decom Files', '*.decom')],
                defaultextension='.decom', initialdir=DIR_LED_DISPLAY_DEFAULT)
        )

        # remove possible previous background
        self.image_canvas.delete(self.id_image_canvas)

        # clear canvas from previous drawn stuff
        self.clear_all_canvas()

        # read parameters
        self.parameters.from_json(dict_simu)
        logging.debug(f"Parameters: {self.parameters}")
        self.set_led_variables()

        logging.debug(f'Opening simulation at {self.parameters["simu_dest_path"]}')
        self.open_image(self.parameters["image_src_path"])

        # update vars
        self.draw_referential_line()
        logging.debug("Referential line: OK")
        self.import_led_strips()
        logging.debug("LED Strips: OK")

    def save_simulation_to_file(self):
        # file format : .decom
        self.parameters["simu_dest_path"] = filedialog.asksaveasfilename(initialfile='simulation-1',
                                                                         defaultextension=".decom",
                                                                         filetypes=[("Decom Files", "*.decom")],
                                                                         initialdir=DIR_LED_DISPLAY_DEFAULT)
        FileUtils.save_simulation_to_file(self.parameters)
        logging.debug(f'Saving simulation to {self.parameters["simu_dest_path"]}')

    def remove_obj_from_canvas(self, id_obj):
        self.image_canvas.delete(id_obj)

    def undo_last_draw(self):
        logging.debug("Undo last led strip drawn")
        if len(self.parameters["led_strips"]) != 0:
            obj_to_del = self.parameters["led_strips"].pop()
            ids_to_del = obj_to_del.delete_object()
            [self.remove_obj_from_canvas(id_del) for id_del in ids_to_del]

    def remove_objs_from_canvas(self, list_ids: list[int]):
        logging.debug("Removing all objects given from canvas")
        [self.remove_obj_from_canvas(id_obj) for id_obj in list_ids]

    def clear_canvas(self, option=DRAWING):
        logging.debug("Clearing canvas based on option given")
        if option == DRAWING:
            for led_strip in self.parameters["led_strips"]:
                [self.remove_obj_from_canvas(id_obj) for id_obj in led_strip.delete_object()]

            self.parameters["led_strips"] = []

        elif option == MEASURING:
            self.image_canvas.delete(self.parameters["referential"].remove_from_canvas())
            self.remove_label_ref()

    def clear_all_canvas(self):
        logging.debug("Clearing canvas from referential line and led strips")
        self.clear_canvas(DRAWING)
        self.clear_canvas(MEASURING)

    def button_1_released(self, event):
        self.add_line(event)
        if self.mode.get() == MEASURING:
            logging.debug(
                f'Adding referential line between {self.parameters["referential"].get("x_src"), self.parameters["referential"].get("y_src")} and {self.parameters["referential"].get("x_dest"), self.parameters["referential"].get("y_dest")}')
            self.measuring = False

        elif self.mode.get() == DRAWING:
            logging.debug("Adding LED strip line")
            self.parameters.add_led_strip(self.current_drawing_strip.copy())
            self.current_drawing_strip = []

    def button_1_pressed(self, event):
        if self.mode.get() == DRAWING:
            self.last_x, self.last_y = event.x, event.y

        elif self.mode.get() == MEASURING and not self.measuring:
            self.parameters["referential"].set_origin(event.x, event.y)
            self.measuring = True

        self.update_position(event)

    def import_led_strips(self):
        # instead of calculating new positions and stuff, just add new led to canvas
        self.draw_led_lines()
        self.draw_led_strips()

    def draw_led(self, led: LED):
        logging.debug(f"LED to draw: {led}")
        x0, y0, x1, y1 = led.get_rect_coordinates()
        color = led.get("color")

        id_led = self.image_canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        return id_led

    def draw_led_strip(self, index_led_strip):
        for i_led, led in enumerate(self.parameters["led_strips"][index_led_strip]["list_leds"]):
            id_led_canvas = self.draw_led(led)
            self.parameters["led_strips"][index_led_strip].update_id_led_canvas_at_index(i_led, id_led_canvas)

    def draw_led_strips(self):
        for index_l_strip in range(len(self.parameters["led_strips"])):
            self.draw_led_strip(index_l_strip)

    def generate_led_strips(self):
        logging.debug("Generating LED strips")
        prev_strip_index, prev_led_index, prev_led_id = -1, -1, None

        for i in range(len(self.parameters["led_strips"])):
            # remove previous leds from canvas, LEDStrip list
            self.remove_objs_from_canvas(self.parameters["led_strips"][i].remove_leds())
            # calculate new led positions based on LED density and LED size
            self.parameters["led_strips"][i].calculate_led_positions(
                self.parameters["referential"]["ratio_px_to_mm"],
                self.led_density_var.get(), self.led_size_px_var.get())

            # add leds to canvas
            for j, led in enumerate(self.parameters["led_strips"][i]["list_leds"]):
                id_led_canvas = self.draw_led(led)

                # exchange information between LEDs and strips
                self.parameters["led_strips"][i].update_id_led_canvas_at_index(j, id_led_canvas)
                id_led = self.parameters["led_strips"][i].get_id_led_at_index(j)
                if prev_led_id is not None:
                    self.parameters["led_strips"][i].add_prev_id_to_led(j, prev_led_id)
                    self.parameters["led_strips"][prev_strip_index].add_next_id_to_led(prev_led_index,
                                                                                       id_led)

                prev_strip_index, prev_led_index, prev_led_id = i, j, id_led

    def draw_line(self, x_src=None, y_src=None, x_dest=None, y_dest=None, fill=None, width=1, tags=DRAWING, dash=None,
                  arrow=None, smooth=False) -> int:
        logging.debug(
            f"Drawing line between: {x_src, y_src}, and {x_dest, y_dest} / fill={fill} / width={width} px / tags={tags} / dash={dash} / arrow={arrow}")

        if dash is not None:
            dash = tuple(dash)

        return self.image_canvas.create_line(
            x_src,
            y_src,
            x_dest,
            y_dest,
            fill=fill,
            width=width,
            tags=tags,
            dash=dash,
            arrow=arrow,
            smooth=smooth
        )

    def add_line(self, event):
        if self.parameters["app_mode"] == DRAWING:
            line_id = self.draw_line(self.last_x, self.last_y, event.x, event.y, fill="red", width=1, tags=DRAWING,
                                     smooth=True)
            self.current_drawing_strip.append([line_id, [self.last_x, self.last_y, event.x, event.y]])

            self.last_x, self.last_y = event.x, event.y
        elif self.parameters["app_mode"] == MEASURING:
            self.parameters["referential"].set("x_dest", event.x)
            self.parameters["referential"].set("y_dest", event.y)
            self.draw_referential_line()

    def remove_referential_elements(self):
        self.remove_obj_from_canvas(self.parameters["referential"]["id_line_canvas"])
        self.remove_label_ref()

    def draw_referential_line(self):
        logging.debug("Drawing referential line")
        self.remove_referential_elements()

        self.parameters["referential"]["id_line_canvas"] = self.draw_line(
            self.parameters["referential"]["x_src"],
            self.parameters["referential"]["y_src"],
            self.parameters["referential"]["x_dest"],
            self.parameters["referential"]["y_dest"],
            fill=self.parameters["referential"]["fill"],
            width=self.parameters["referential"]["width"],
            tags=self.parameters["referential"]["tags"],
            dash=self.parameters["referential"]["dash"],
            arrow=self.parameters["referential"]["arrow"]
        )

        self.update_label_ref()

    def draw_led_lines(self):
        logging.debug("Drawing LED lines")
        logging.debug(f'LED strips: {self.parameters["led_strips"]}')

        # get led strips
        for index_led_strip, led_strip in enumerate(self.parameters["led_strips"]):
            logging.debug(f"LED Strip index: {index_led_strip}")
            # get led lines
            for index_line, led_strip_line in enumerate(self.parameters["led_strips"][index_led_strip]["lines_canvas"]):
                logging.debug(f"LED Strip line: {led_strip_line}")
                # draw lines
                _, [x_src, y_src, x_dest, y_dest] = led_strip_line
                id_line = self.draw_line(x_src, y_src, x_dest, y_dest, led_strip.get("fill"), led_strip.get("width"),
                                         DRAWING)
                self.parameters["led_strips"][index_led_strip]["lines_canvas"][index_line][0] = id_line

    """
    UPDATE FUNCTIONS
    """

    def set_led_variables(self):
        logging.debug("Setting LED variables on application window")
        self.led_density_var.set(self.parameters["led_density"])
        self.led_size_px_var.set(self.parameters["led_size_px"])

    def update_leds(self, new_value):
        logging.debug("Updating LED strips")
        self.parameters["led_size_px"] = self.led_size_px_var.get()
        self.parameters["led_density"] = self.led_density_var.get()
        self.generate_led_strips()

    def update_position(self, event=None):
        self.cursor_pos_var.set(f"Position: ({event.x}, {event.y})")
        self.cursor_pos_label.update()

    def update_mode(self):
        logging.debug("Updating drawing mode")
        if self.mode.get() == DRAWING:
            for child in self.frame_measuring.winfo_children():
                child.configure(state='disable')
            for child in self.frame_drawing.winfo_children():
                child.configure(state='normal')
            self.parameters["app_mode"] = DRAWING

        if self.mode.get() == MEASURING:
            for child in self.frame_measuring.winfo_children():
                child.configure(state='normal')
            for child in self.frame_drawing.winfo_children():
                child.configure(state='disable')
            self.parameters["app_mode"] = MEASURING

    def remove_label_ref(self):
        self.label_ref.destroy()

    def update_label_ref(self):
        self.remove_label_ref()
        self.label_ref = Label(self.frame_image,
                               text=f'{self.parameters["referential"]["dist_mm_src_to_dest"]} mm')
        self.label_ref.place(
            x=(self.parameters["referential"]["x_src"] + self.parameters["referential"]["x_dest"]) / 2 - 30,
            y=(self.parameters["referential"]["y_src"] + self.parameters["referential"]["y_dest"]) / 2 + 10)

    def update_label_ref_ratio(self):
        self.px_to_mm_label.config(text=f'1 px = {self.parameters["referential"]["ratio_px_to_mm"]} mm')

    def update_label_ref_callback(self, var, index, mode):
        try:
            var = self.distance_mm_var.get()
        except TclError:
            var = 0
        self.parameters["referential"].set("dist_mm_src_to_dest", var)
        self.update_label_ref_ratio()
        self.update_label_ref()

    def update_description(self):
        logging.debug("Updating description")
        # TODO description not properly updated
        pass

    def update_all_variables_and_fields(self, var=None, index=None, mode=None):
        logging.debug("Updating all variables")
        # drawing or measuring
        self.update_mode()
        # update LEDs based on density and display size
        self.update_leds(var)
        # updating ref label on canvas measure and ref label in frame referential
        self.update_label_ref_callback(var, index, mode)
        # updating description
        self.update_description()
