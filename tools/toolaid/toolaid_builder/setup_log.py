"""
Set up logging
"""

import os
import yaml
import logging
import logging.config

config_file = os.path.join(os.path.dirname(__file__), 'logging.yaml')

with open(config_file) as f:
    logging_config = yaml.load(f)
    logging.config.dictConfig(logging_config)



    
