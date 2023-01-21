from src import PhasmoPresence
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s')
    handler = logging.FileHandler('PhasmoPresence.log')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    client = PhasmoPresence(client_id='super')
    client.run()
