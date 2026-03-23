import logging
from web3 import Web3
from config.settings import settings

logger = logging.getLogger(__name__)

class BlockchainConnection:
    def __init__(self):
        self.w3_http = Web3(Web3.HTTPProvider(settings.ETH_HTTP_URL))
        
        if settings.ETH_WSS_URL:
            self.w3_wss = Web3(Web3.WebsocketProvider(settings.ETH_WSS_URL))
        else:
            self.w3_wss = None

    def is_connected(self) -> bool:
        return self.w3_http.is_connected()

    def get_http_provider(self):
        return self.w3_http
        
    def get_wss_provider(self):
        return self.w3_wss

ethereum_conn = BlockchainConnection()
