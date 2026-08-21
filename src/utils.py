import logging
from urllib.parse import urljoin
import requests
import json
from typing import Any, Dict, List


def obtener_html(url: str) -> str:
    """
    Descarga el HTML de una URL.
    """

    try:
        respuesta = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/139.0 Safari/537.36"
                )
            },
        )

        respuesta.raise_for_status()

        return respuesta.content.decode(
            respuesta.encoding or "utf-8",
            errors="replace",
        )

    except requests.RequestException:
        logging.exception(
            "Error al obtener la URL: %s",
            url,
        )
        return ""


def obtener_url(href: str, url_base: str) -> str:
    """
    Convierte una URL relativa en absoluta.
    """

    if not href:
        return ""

    return urljoin(
        url_base,
        href,
    )


def limpiar_texto(elemento) -> str:
    """
    Extrae y limpia el texto de un elemento lxml.
    """

    if elemento is None:
        return ""

    if hasattr(elemento, "text_content"):
        texto = elemento.text_content()
    else:
        texto = str(elemento)

    return " ".join(
        texto.split()
    )

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