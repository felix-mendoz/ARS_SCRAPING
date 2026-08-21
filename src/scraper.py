import logging
from typing import Any, Dict, List
from .utils import obtener_html, limpiar_texto, obtener_url
from lxml import html


# ============================================================================
# XPATH
# ============================================================================

# Página principal
XPATH_ELEMENTOS = (
    '//*[@id="main-content"]/div/div/div[2]'
)

XPATH_ENLACE = ".//a[@href][1]"


# ============================================================================
# PÁGINA INDIVIDUAL
# ============================================================================

XPATH_CONTENEDOR = (
    '//*[@id="main-content"]/div/div/div[1]'
)

XPATH_NOMBRE = (
   'div[1]/div/div[2]/div/div/div[1]/h2'
)

XPATH_RNC = (
    'div[2]/div[2]/div[6]/div/div/div[1]/p'
)

XPATH_TELEFONO = (
    'div[2]/div[3]/div[4]/div/div/div[1]/p'
)

XPATH_CORREO = (
    'div[2]/div[3]/div[6]/div/div/div[1]/span'
)

XPATH_PAGINA_WEB = (
    'div[2]/div[1]/div[2]/div'
)


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def obtener_documento(url: str):
    """
    Descarga una página y la convierte en un documento lxml.
    """
    contenido = obtener_html(url)

    if not contenido:
        return None

    try:
        return html.fromstring(contenido)
    except Exception:
        logging.exception(
            "No se pudo convertir el HTML a documento XPath: %s",
            url,
        )
        return None


def obtener_primer_elemento(elemento, xpath: str):
    """
    Ejecuta un XPath y devuelve el primer elemento encontrado.
    """
    resultados = elemento.xpath(xpath)

    if not resultados:
        return None

    return resultados[0]


def extraer_texto_xpath(elemento, xpath: str) -> str:
    """
    Busca un elemento mediante XPath y extrae su texto.
    """
    resultado = obtener_primer_elemento(elemento, xpath)

    if resultado is None:
        return ""

    return limpiar_texto(resultado)


def extraer_href_xpath(elemento, xpath: str) -> str:
    """
    Busca un enlace mediante XPath y devuelve su href.
    """
    resultado = obtener_primer_elemento(elemento, xpath)

    if resultado is None:
        return ""

    href = resultado.get("href")

    if not href:
        return ""

    return href.strip()


def extraer_datos(url: str) -> List[Dict[str, Any]]:
    """
    Extrae los datos de las empresas desde la página principal.

    Estructura esperada:

        sección
        └── fila
            ├── elemento/div -> enlace -> página individual
            ├── elemento/div -> enlace -> página individual
            ├── elemento/div -> enlace -> página individual
            └── ...

    Primero se recorren las filas y, dentro de cada fila,
    se recorren todos los div que contienen los enlaces.

    Todo el procesamiento DOM se realiza mediante XPath usando lxml.
    """

    resultados: List[Dict[str, Any]] = []

    # =========================================================================
    # PÁGINA PRINCIPAL
    # =========================================================================

    documento = obtener_documento(url)

    if documento is None:
        logging.error(
            "No se pudo obtener la página principal: %s",
            url,
        )
        return resultados

    # -------------------------------------------------------------------------
    # Buscar sección principal
    # -------------------------------------------------------------------------

    secciones = documento.xpath(XPATH_ELEMENTOS)

    if not secciones:
        logging.error(
            "No se encontró la sección de elementos en la página principal."
        )
        return resultados

    logging.info(
        "Se encontraron %d sección(es) de elementos.",
        len(secciones),
    )

    # =========================================================================
    # RECORRER LAS SECCIONES
    # =========================================================================

    for numero_seccion, seccion in enumerate(secciones, start=1):

        logging.info(
            "Procesando sección %d de %d.",
            numero_seccion,
            len(secciones),
        )

        # ---------------------------------------------------------------------
        # Obtener las filas de la sección
        # ---------------------------------------------------------------------

        filas = seccion.xpath("./div")

        if not filas:
            logging.warning(
                "No se encontraron filas en la sección %d.",
                numero_seccion,
            )
            continue

        logging.info(
            "Se encontraron %d filas en la sección %d.",
            len(filas),
            numero_seccion,
        )

        # =====================================================================
        # RECORRER CADA FILA
        # =====================================================================

        for numero_fila, fila in enumerate(filas, start=1):

            logging.info(
                "Procesando fila %d de %d en la sección %d.",
                numero_fila,
                len(filas),
                numero_seccion,
            )

            # -----------------------------------------------------------------
            # Cada fila contiene múltiples div.
            # Cada uno de esos div representa un elemento/empresa.
            # -----------------------------------------------------------------

            elementos = fila.xpath("./div")

            if not elementos:
                logging.warning(
                    "No se encontraron elementos en la fila %d "
                    "de la sección %d.",
                    numero_fila,
                    numero_seccion,
                )
                continue

            logging.info(
                "La fila %d contiene %d elementos.",
                numero_fila,
                len(elementos),
            )

            # =================================================================
            # RECORRER CADA ELEMENTO DE LA FILA
            # =================================================================

            for numero_elemento, elemento in enumerate(elementos, start=1):

                logging.info(
                    "Procesando elemento %d de %d "
                    "(fila %d, sección %d).",
                    numero_elemento,
                    len(elementos),
                    numero_fila,
                    numero_seccion,
                )

                # -------------------------------------------------------------
                # Buscar enlace dentro del elemento
                # -------------------------------------------------------------

                href = extraer_href_xpath(
                    elemento,
                    XPATH_ENLACE,
                )

                if not href:
                    logging.warning(
                        "El elemento %d de la fila %d "
                        "no contiene ningún enlace.",
                        numero_elemento,
                        numero_fila,
                    )
                    continue

                # -------------------------------------------------------------
                # Construir URL absoluta
                # -------------------------------------------------------------

                ars_url = obtener_url(
                    href,
                    url,
                )

                if not ars_url:
                    logging.warning(
                        "No se pudo construir la URL del elemento %d "
                        "de la fila %d.",
                        numero_elemento,
                        numero_fila,
                    )
                    continue

                logging.info(
                    "Visitando elemento %d/%d de la fila %d: %s",
                    numero_elemento,
                    len(elementos),
                    numero_fila,
                    ars_url,
                )

                # =============================================================
                # PÁGINA INDIVIDUAL
                # =============================================================

                ars = obtener_documento(ars_url)

                if ars is None:
                    logging.warning(
                        "No se pudo obtener la página: %s",
                        ars_url,
                    )
                    continue

                # -------------------------------------------------------------
                # Buscar contenedor de los datos
                # -------------------------------------------------------------

                contenedor = obtener_primer_elemento(
                    ars,
                    XPATH_CONTENEDOR,
                )

                if contenedor is None:
                    logging.warning(
                        "No se encontró el contenedor esperado en: %s",
                        ars_url,
                    )
                    continue

                # =============================================================
                # EXTRAER DATOS
                # =============================================================

                nombre = extraer_texto_xpath(
                    contenedor,
                    XPATH_NOMBRE,
                )

                telefono = extraer_texto_xpath(
                    contenedor,
                    XPATH_TELEFONO,
                )

                correo = extraer_texto_xpath(
                    contenedor,
                    XPATH_CORREO,
                )

                rnc = extraer_texto_xpath(
                    contenedor,
                    XPATH_RNC,
                )

                pagina_web = extraer_texto_xpath(
                    contenedor,
                    XPATH_PAGINA_WEB,
                )

                # =============================================================
                # RESULTADO
                # =============================================================

                item = {
                    "nombre": nombre,
                    "telefono": telefono,
                    "correo": correo,
                    "rnc": rnc,
                    "pagina_web": pagina_web,
                    "url": ars_url,
                }

                resultados.append(item)

                logging.info(
                    "Empresa extraída correctamente: %s",
                    nombre or "(sin nombre)",
                )

    # =========================================================================
    # FINAL
    # =========================================================================

    logging.info(
        "Extracción finalizada. Registros obtenidos: %d",
        len(resultados),
    )

    return resultados