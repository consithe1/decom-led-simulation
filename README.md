# LED Simulation and Display Tool (LSD-T)

## Description
This project is to simulate LED strips and run animations in order to visualise them 
before implementing them IRL.

## Functionalities

### Define a referential
> A referential is an object that makes the equivalence between distances in real life
(in *mm*) and distances in the program (in *px*)

In order to define it, a few features are available:
- drawing a reference line (represented as a blue dashed line)
- defining the reference line length (in *mm*)

### LED Displays

> A LED Display is an aggregation of LED strips (nd. a LED display can contain 
just one LED strip).

In this simulation, a LED display is just a `list` of LED Strips.

### LED Strips

> A LED Strip is an aggregation of LEDs (nd. a LED strip can contain just one LED)

This object has a few parameters but the major ones are the `lines` and the `LEDs`. 
These parameters are represented has `list` objects in the simulation.

A line is represented as follows: `[id_line_on_canvas, [x0, y0, x1, y1]]`

### Import / Save LED Display
Once a LED display has been created or modified, it can be saved to a `.decom` file. 
The same way it is saved, it can be imported in the application by selecting a valid `.decom` file.

### LED Sequences

> A LED sequence is defined as bytes of data to give to the LEDs to display something



## To implement
- `.decom` import verifications
- add zoom-in and zoom-out features when drawing on canvas

## Known Issues
- Updating the distance in mm doesn't actualise properly the LED display
- Images are not properly resized when imported : need to resize the image and center it on the canvas
- "Clear All" button doesn't remove the referential line