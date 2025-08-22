from __future__ import annotations

from .bambu import BambuConnector
from .octoprint import OctoPrintConnector
from .base import PrinterConnector
from ..config import settings


def get_connector(provider: str) -> PrinterConnector:
    if provider == "bambu":
        return BambuConnector(settings.bambu_connect_api_key)
    if provider == "octoprint":
        return OctoPrintConnector(
            settings.octoprint_base_url, settings.octoprint_api_key
        )
    raise ValueError("unknown provider")


__all__ = ["get_connector", "PrinterConnector"]

