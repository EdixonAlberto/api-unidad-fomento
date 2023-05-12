# API Unidad Fomento

![](https://img.shields.io/badge/author-Edixon_Piña-yellow?style=for-the-badge)
![](https://img.shields.io/badge/python-3.8-blue?style=for-the-badge)

![banner](docs/banner.jpg)

API Rest para consultar el valor de la unidad de fomento en Chile.

<!-- Documentation &#x279c; **[OpenAPI Specification]()** -->

> NOTA: Este proyecto es la solución del siguiente desafío de código:
> [https://gist.github.com/lhidalgo42/47c2c1ea4ddbfd50e4b0acd82c24bc23](https://gist.github.com/lhidalgo42/47c2c1ea4ddbfd50e4b0acd82c24bc23)

### Inicio

Antes de comenzar a desarrollar debe instalar pipenv con pip, luego instalar las dependencias y copiar el
[template](./.env.template) con las variables de entorno en la raiz del proyecto, luego podrá ejecutar el script
`start`.

```sh
pip install pipenv
pipenv shell
pipenv install --dev
cp .env.template .env
pipenv run start
```

### Endpoints

| Endpoint                 | HTTP | Description                                                     | Query Params     |
| ------------------------ | ---- | --------------------------------------------------------------- | ---------------- |
| 🔒 `/api/status`         | GET  | Obtener estatus de la api                                       |                  |
| 🔒 `/api/unidad_fomento` | GET  | Obtener valor de la unidad de fomento para una fecha específica | ?date=01-01-2013 |

### Ejemplo

```json
// Respuesta de: {HOST}/api/unidad_fomento?date=01-01-2013
{
  "errors": [],
  "response": {
    "query_date_timestamp": "2013-01-01T00:00:00.000000Z",
    "unit": 22837.06,
    "unit_string": "22.837,06"
  },
  "status_code": 200
}
```

### Comandos

```sh
# Preparar el entorno virtual para python
pipenv shell

# Instalar todas las dependencias descritas en Pipfile
pipenv install --dev

# Ejecutar la API
pipenv run start

# Ejecutar todos los test ubicados en ./tests
pipenv run test
```

### Despliegue

Para desplegar esta API primero se debe instalar las depedencias en sus versiones específicas a travez del archivo
[requirements.txt](./requirements.txt) y luego ejecutar el servidor ejcutando el archivo `run.py`

```sh
pip install -r requirements.txt
python run.py
```

> NOTA: Este proyecto ha sido construido y probado usando el siguiente conjunto de tecnologías:

- Python v3.8.10
- flask
- autopep8
- flask-restx
- pytest
- beautifulsoup4

### License

[MIT](./LICENSE) &copy; Edixon Piña
