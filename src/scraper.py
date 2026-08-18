# scraper.py
import logging
from typing import Any, Dict, List
from .utils import obtener_soup, limpiar_texto, obtener_url

# ============================================================================
# SELECTORES
# ============================================================================

SELECTOR_ELEMENTOS = (
    "#main-content > div > div > "
    "div.et_pb_section.et_pb_section_1_tb_body.et_section_regular"
)

SELECTOR_CONTENEDOR = (
    "#main-content > div > div > "
    "div.et_pb_section.et_pb_section_0_tb_body."
    "et_section_regular.section_has_divider.et_pb_bottom_divider"
)

SELECTOR_NOMBRE = (
    "#main-content > div > div > "
    "div.et_pb_section.et_pb_section_0_tb_body."
    "et_section_regular.section_has_divider.et_pb_bottom_divider "
    "> div.et_pb_row.et_pb_row_0_tb_body "
    "> div > div.et_pb_module.et_pb_de_mach_acf_item."
    "et_pb_de_mach_acf_item_0_tb_body."
    "dmach-text-before-pos-same_line."
    "dmach-label-pos-same_line."
    "dmach-vertical-alignment-middle."
    "et_pb_de_mach_alignment_.dmach-acf-has-value."
    "dmach-image-icon-placement-left "
    "> div > div > div.dmach-acf-item-content > h2"
)

SELECTOR_TELEFONO = (
    "#main-content > div > div > "
    "div.et_pb_section.et_pb_section_0_tb_body."
    "et_section_regular.section_has_divider.et_pb_bottom_divider "
    "> div.et_pb_row.et_pb_row_1_tb_body."
    "et_pb_row_1-2_1-4_1-4 "
    "> div.et_pb_column.et_pb_column_1_4."
    "et_pb_column_3_tb_body."
    "et_pb_css_mix_blend_mode_passthrough.et-last-child "
    "> div.et_pb_module.et_pb_de_mach_acf_item."
    "et_pb_de_mach_acf_item_6_tb_body."
    "dmach-text-before-pos-same_line."
    "dmach-label-pos-same_line."
    "dmach-vertical-alignment-middle."
    "et_pb_de_mach_alignment_.dmach-acf-has-value."
    "dmach-image-icon-placement-left "
    "> div > div > div.dmach-acf-item-content > p"
)

SELECTOR_CORREO = (
    "#main-content > div > div > "
    "div.et_pb_section.et_pb_section_0_tb_body."
    "et_section_regular.section_has_divider.et_pb_bottom_divider "
    "> div.et_pb_row.et_pb_row_1_tb_body."
    "et_pb_row_1-2_1-4_1-4 "
    "> div.et_pb_column.et_pb_column_1_4."
    "et_pb_column_3_tb_body."
    "et_pb_css_mix_blend_mode_passthrough.et-last-child "
    "> div.et_pb_module.et_pb_de_mach_acf_item."
    "et_pb_de_mach_acf_item_7_tb_body."
    "dmach-text-before-pos-same_line."
    "dmach-label-pos-same_line."
    "dmach-vertical-alignment-middle."
    "et_pb_de_mach_alignment_.dmach-acf-has-value."
    "dmach-image-icon-placement-left "
    "> div > div > div.dmach-acf-item-content > span"
)

SELECTOR_RNC = (
    "#main-content > div > div > "
    "div.et_pb_section.et_pb_section_0_tb_body."
    "et_section_regular.section_has_divider.et_pb_bottom_divider "
    "> div.et_pb_row.et_pb_row_1_tb_body."
    "et_pb_row_1-2_1-4_1-4 "
    "> div.et_pb_column.et_pb_column_1_4."
    "et_pb_column_2_tb_body."
    "et_pb_css_mix_blend_mode_passthrough "
    "> div.et_pb_module.et_pb_de_mach_acf_item."
    "et_pb_de_mach_acf_item_4_tb_body."
    "dmach-text-before-pos-same_line."
    "dmach-label-pos-same_line."
    "dmach-vertical-alignment-middle."
    "et_pb_de_mach_alignment_.dmach-acf-has-value."
    "dmach-image-icon-placement-left "
    "> div > div > div.dmach-acf-item-content > p"
)

SELECTOR_PAGINA_WEB = (
    "#main-content > div > div > "
    "div.et_pb_section.et_pb_section_0_tb_body."
    "et_section_regular.section_has_divider.et_pb_bottom_divider "
    "> div.et_pb_row.et_pb_row_1_tb_body."
    "et_pb_row_1-2_1-4_1-4 "
    "> div.et_pb_column.et_pb_column_1_2."
    "et_pb_column_1_tb_body."
    "et_pb_css_mix_blend_mode_passthrough "
    "> div.et_pb_module.et_pb_text."
    "et_pb_text_1_tb_body.et_clickable."
    "et_pb_text_align_center.et_pb_bg_layout_light "
    "> div"
)


def extraer_datos(url: str) -> List[Dict[str, Any]]:
    """
    Extrae los datos de las empresas desde la página principal
    y posteriormente visita la página individual de cada empresa.
    """

    soup = obtener_soup(url)

    if not soup:
        logging.error("No se pudo obtener la página principal.")
        return []

    resultados = []

    # =========================================================================
    # PÁGINA PRINCIPAL
    # =========================================================================

    seccion = soup.select_one(SELECTOR_ELEMENTOS)

    if not seccion:
        logging.error("No se encontró la sección de elementos en la página principal.")
        return []

    filas = seccion.select(":scope > div.et_pb_row")

    if not filas:
        logging.error("No se encontraron filas en la sección de elementos.")
        return []

    # =========================================================================
    # PROCESAR CADA FIla
    # =========================================================================

    for  fila in filas:

        elementos = fila.select(":scope > div.et_pb_column")

        if not elementos:
            logging.warning("No se encontraron elementos en la fila.")
            continue

        for numero, elemento in enumerate(elementos, start=1):

            logging.info(
                "Procesando elemento %d de %d",
                numero,
                len(elementos),
            )

            # ---------------------------------------------------------------------
            # Obtener URL de la página individual
            # ---------------------------------------------------------------------

            enlace_elemento = elemento.select_one("a")

            if not enlace_elemento:
                logging.warning(
                    "El elemento %d no contiene ningún enlace.",
                    numero,
                )
                continue

            ars_url = obtener_url(
                enlace_elemento,
                url,
            )

            if not ars_url:
                logging.warning(
                    "No se pudo obtener la URL del elemento %d.",
                    numero,
                )
                continue

            logging.info("Visitando: %s", ars_url)

            # ---------------------------------------------------------------------
            # Obtener página individual
            # ---------------------------------------------------------------------

            ars = obtener_soup(ars_url)

            if not ars:
                logging.warning(
                    "No se pudo obtener la página: %s",
                    ars_url,
                )
                continue

            # ---------------------------------------------------------------------
            # Verificar que exista el contenedor esperado
            # ---------------------------------------------------------------------

            contenedor = ars.select_one(SELECTOR_CONTENEDOR)

            if not contenedor:
                logging.warning(
                    "No se encontró el contenedor esperado en: %s",
                    ars_url,
                )
                continue

            # ---------------------------------------------------------------------
            # Extraer datos
            # ---------------------------------------------------------------------

            nombre = limpiar_texto(
                ars.select_one(
                    SELECTOR_NOMBRE
                )
            )

            telefono = limpiar_texto(
                ars.select_one(
                    SELECTOR_TELEFONO
                )
            )

            correo = limpiar_texto(
                ars.select_one(
                    SELECTOR_CORREO
                )
            )

            rnc = limpiar_texto(
                ars.select_one(
                    SELECTOR_RNC
                )
            )

            pagina_web = limpiar_texto(
                ars.select_one(
                    SELECTOR_PAGINA_WEB
                )
            )

            # ---------------------------------------------------------------------
            # Objeto final
            # ---------------------------------------------------------------------

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
        "Extracción finalizada. Registros obtenidos: %d",
        len(resultados),
    )

    return resultados