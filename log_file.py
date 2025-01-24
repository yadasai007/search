import logging
from datetime import datetime
file_directory="E:\\search\\logs\\"
filename=datetime.now().strftime("%Y-%m-%d")+'.log'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(file_directory+filename)]
                    )
logger = logging.getLogger(__name__)