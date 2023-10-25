from src.simulation import LEDSimulator
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', filename="logs/simulation.log", level=logging.DEBUG, filemode='w')

    app = LEDSimulator()
    app.mainloop()
