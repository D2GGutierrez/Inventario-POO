# Inventario-POO

Sistema de inventario desarrollado con Django (Python 3.13) para la materia de POO.

## Estructura

```
Inventario-POO/
├── config/            # Configuración del proyecto (settings, urls, wsgi/asgi)
inventario/
├── migrations/
│
├── models.py          ← entidades + lógica del dominio
├── views.py           ← CBV
├── urls.py
├── admin.py
├── tests.py
│
├── forms.py           ← siguiente expansión interesante
├── services.py        ← lógica compleja de inventario
│
├── templates/
│   └── inventario/
│       ├── producto_list.html
│       ├── producto_detail.html
│       ├── producto_form.html
│       ├── movimiento_list.html
│       └── movimiento_form.html
│
└── static/
    └── inventario/
        ├── css/
        └── js/
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

## Modelos principales

| Modelo       | Descripción                                            |
|--------------|--------------------------------------------------------|
| `Categoria`  | Agrupa productos                                       |
| `Proveedor`  | Proveedores asociados a productos (M2M)                |
| `Producto`   | SKU, precio, stock, stock mínimo y alerta de resurtido |
| `Movimiento` | Entradas/salidas que ajustan el stock automáticamente  |
| `ModeloBase` | Clase abstracta con timestamps (`creado`, `actualizado`)|

## Puesta en marcha

```bash
# 1. Crear entorno virtual
py -3.13 -m venv .venv

# 2. Activar (Windows PowerShell)
.venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Migraciones y superusuario
python manage.py migrate
python manage.py createsuperuser

# 5. Levantar el servidor
python manage.py runserver
```

## Tests

```bash
python manage.py test inventario
```
