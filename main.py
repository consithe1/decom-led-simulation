from src.simulation import LEDSimulator
import logging.config
import logging
import coloredlogs
import os
import yaml


def setup_logging(default_path='../logging.yaml', default_level=logging.DEBUG, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value

    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Failed to load configuration file. Using default configs')


if __name__ == '__main__':
    setup_logging()

    app = LEDSimulator()
    app.mainloop()
