import yaml

class UserContext(object):
    def __init__(self, config_path=None, verbose=False):
        self.verbose = verbose
        self.config_path = config_path
        self.data = self.load_data() if self.config_path else None

    def load_data(self):
        with open(self.config_path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                pass