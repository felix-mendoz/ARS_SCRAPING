from src.scraper import extraer_datos
from src.utils import guardar_json
import logging

logging.basicConfig(level=logging.INFO)

def main():
    url = "https://www.sisalril.gob.do/supervisados/"
    datos = extraer_datos(url)

    if datos:
        logging.info("Datos extraídos correctamente.")
        guardar_json(datos, "data/aseguradoras.json")
    else:
        logging.warning("No se extrajeron datos.")

if __name__ == "__main__":
    main()