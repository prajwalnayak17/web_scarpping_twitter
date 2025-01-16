import random
import logging
from typing import Dict, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ProxyMeshConfig:
    username: str
    password: str
    port: int = 31280


class ProxyManager:
    def __init__(self, config: ProxyMeshConfig):
        self.config = config
        self.proxy_locations = [
            'us-wa',
            'us-fl',
            'us-ny',
            'uk',
            'de',
            'jp',
            'sg'
        ]

    def get_random_proxy(self) -> Dict[str, str]:
        """Get a random proxy configuration with authentication"""
        try:
            location = random.choice(self.proxy_locations)
            proxy_url = (
                f"http://{self.config.username}:{self.config.password}@"
                f"{location}.proxymesh.com:{self.config.port}"
            )

            proxy_config = {
                "http": proxy_url,
                "https": proxy_url
            }

            logger.info(f"Generated proxy configuration for location: {location}")
            return proxy_config

        except Exception as e:
            logger.error(f"Error generating proxy configuration: {str(e)}")
            raise

    def get_proxy_selenium_options(self) -> dict[str, dict[str, str]]:
        """Get proxy configuration formatted for Selenium"""
        proxy_config = self.get_random_proxy()
        return {
            "proxy": {
                "httpProxy": proxy_config["http"],
                "sslProxy": proxy_config["https"],
                "proxyType": "MANUAL"
            }
        }