# utils.py
import json
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}

def obtener_soup(url: str) -> Optional[BeautifulSoup]:
    """
    Realiza una petición HTTP y devuelve el HTML convertido
    en un objeto BeautifulSoup.
    """
    try:
        logging.info("Obteniendo: %s", url)

        respuesta = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
        )

        respuesta.raise_for_status()

        return BeautifulSoup(respuesta.text, "html.parser")

    except requests.RequestException as e:
        logging.error("Error al obtener %s: %s", url, e)
        return None

def limpiar_texto(elemento) -> str:
    """
    Extrae texto de un elemento HTML de forma segura.
    """
    if not elemento:
        return ""

    return elemento.get_text(" ", strip=True)

def obtener_url(elemento, url_base: str = "") -> str:
    """
    Obtiene el href de un elemento <a> y lo convierte
    en URL absoluta si es necesario.
    """
    if not elemento:
        return ""

    href = elemento.get("href", "")

    if not href:
        return ""

    return urljoin(url_base, href)

def guardar_json(
    datos: List[Dict[str, Any]],
    archivo: str = "resultados.json",
) -> None:
    """
    Guarda los datos extraídos en JSON.
    """
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(
                datos,
                f,
                ensure_ascii=False,
                indent=4,
            )

        logging.info(
            "Se guardaron %d registros en %s",
            len(datos),
            archivo,
        )

    except IOError as e:
        logging.error("Error guardando JSON: %s", e)