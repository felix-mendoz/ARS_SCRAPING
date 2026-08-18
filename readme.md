# ARS Scraping Dominican Republic 🇩🇴

Este proyecto consiste en una herramienta de web scraping desarrollada en Python para extraer, estructurar y exportar la información pública y oficial de las Administradoras de Riesgos de Salud (ARS) en la República Dominicana desde el portal oficial de la **Superintendencia de Salud y Riesgos Laborales (SISALRIL)** ([https://www.sisalril.gob.do/](https://www.sisalril.gob.do/)).

## 🎯 Objetivo del Proyecto

El objetivo principal es automatizar la recolección de datos institucionales de las ARS habilitadas y reguladas por la SISALRIL para generar datasets limpios y estructurados en formato **JSON**.

La información extraída incluye:
- Razón Social / Nombre Oficial de la ARS
- Número de RNC (Registro Nacional de Contribuyente)
- Correo electrónico de contacto/atención al afiliado
- Teléfonos institucionales

---

## 📁 Estructura del Proyecto

```text
ARS_SCRAPING/
├── data/                  # Directorio para guardar los JSON extraídos (git ignored)
├── src/
│   ├── scraper.py         # Módulo principal de extracción y scraping
│   └── utils.py           # Funciones auxilares para parseo y limpieza de HTML
├── .gitignore             # Reglas para excluir archivos temporales y datos
├── LICENSE                # Licencia MIT
├── main.py                # Punto de entrada para ejecutar el scraping
├── README.md              # Documentación del proyecto
└── requirements.txt       # Dependencias de Python necesarias