# Sistema de Gestión de Biblioteca (Django)

Proyecto académico hecho con **Django 5** para gestionar **libros, usuarios y préstamos**.  
Incluye interfaz con **Bootstrap 5**, control de disponibilidad de ejemplares, gestión de plazos de devolución, cálculo automático de **multas por retraso** y **CRUD completo** para todas las entidades.

Este sistema fue elaborado como parte del **Entregable 2** de la asignatura **PROGRAMACIÓN PARA CIENCIA DE DATOS** de **UNITEC**, con el objetivo de aplicar conceptos clave de desarrollo web, modelado de datos y lógica de negocio utilizando Python y Django, en un contexto académico y práctico.

---

## 🧭 Características
- **Libros**: alta/edición/eliminación, stock (`ejemplares_totales` y `ejemplares_disponibles`).
- **Usuarios**: alta/edición/eliminación, límite configurable de préstamos (`max_prestamos`).
- **Préstamos**:
  - Registro con validaciones (disponibilidad y límite del usuario).
  - **Devolución** con cálculo automático de **multa** por retraso.
  - Filtro de préstamos **abiertos**.
- Interfaz con **Bootstrap 5** y mensajes de estado.
- Estructura por apps: `libros`, `usuarios`, `prestamos`.

---

## 🧰 Tecnologías
- Python 3.12+
- Django 5.x
- Bootstrap 5 (CDN)

---

## 🚀 Puesta en marcha

### 1) Clonar y crear entorno
```bash
git clone <TU_REPO.git> sistema-gestion-biblioteca
cd sistema-gestion-biblioteca

# Entorno virtual (elige uno)
python3 -m venv .venv && source .venv/bin/activate
# ó
python3 -m pip install --user virtualenv
python3 -m virtualenv .venv && source .venv/bin/activate
```

### 2) Instalar dependencias
```bash
pip install "Django>=5.2"
# (opcional) guardar dependencias
pip freeze > requirements.txt
```

### 3) Configuración rápida
Por defecto se usa SQLite. Ajusta idioma y zona horaria en `sgb/settings.py`:
```python
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Sao_Paulo"
```

### 4) Migraciones y súperusuario
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5) Ejecutar
```bash
python manage.py runserver
```
Ir a: http://127.0.0.1:8000/

---

## 🗂️ Estructura del proyecto
```text
sistema-gestion-biblioteca/
├─ manage.py
├─ sgb/
│  ├─ settings.py
│  └─ urls.py
├─ libros/      # modelos, forms, vistas y urls de Libros
├─ usuarios/    # modelos, forms, vistas y urls de Usuarios
├─ prestamos/   # modelos, forms, vistas y urls de Préstamos
├─ templates/
│  ├─ base.html
│  ├─ home.html
│  ├─ libros/
│  ├─ usuarios/
│  └─ prestamos/
└─ static/
   └─ img/unitec-logo.png
```

---

## 🔗 URLs principales
- **Home**: portada o redirección a Libros (según tu `urls.py`)
- **Libros**: `/libros/`
- **Usuarios**: `/usuarios/`
- **Préstamos**: `/prestamos/`
- **Admin Django**: `/admin/`

---

## 📦 Modelos (resumen)

**libros.Libro**  
Atributos: `titulo`, `autor`, `isbn`, `ejemplares_totales`, `ejemplares_disponibles`  
Métodos: `prestar()`, `devolver()`, `agregar_ejemplares()`

**usuarios.Usuario**  
Atributos: `nombre`, `numero`, `max_prestamos`

**prestamos.Prestamo**  
Atributos: `libro`, `usuario`, `fecha_prestamo`, `fecha_devolucion`, `dias_plazo`, `tarifa_retraso`, `multa`  
Propiedades: `abierta`, `fecha_vencimiento`  
Métodos: `confirmar_prestamo()`, `devolver(fecha)`

---

## 🧑‍💻 Flujo de uso
1. Crea **Usuarios** y **Libros** desde el menú.
2. En **Préstamos → Nuevo**, selecciona libro y usuario, y guarda.
3. Para **devolver**, usa la acción *Devolver*; la multa se calcula automáticamente si hay retraso.

---

## 🖼️ UI
- Bootstrap 5 por CDN en `templates/base.html`.
- Navbar con logo UNITEC (`static/img/unitec-logo.png`).
- Tablas y formularios con clases Bootstrap (`table`, `form-control`, `btn`, etc.).

---

## 8) 🔧 Despliegue (opcional, sin Nginx)

Instala WhiteNoise:
```bash
pip install whitenoise
```

En `settings.py`, agrega en `MIDDLEWARE` (antes de `CommonMiddleware`):
```python
'whitenoise.middleware.WhiteNoiseMiddleware',
```

Define `STATIC_ROOT`:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Recolecta estáticos:
```bash
python manage.py collectstatic
```

---

## 📌 Roadmap
- Buscador en navbar (título/autor/ISBN).
- Filtros de préstamos (abiertos, vencidos) y paginación.
- Exportar a CSV/Excel.
- Autenticación y permisos por rol (bibliotecario/lector).
- Tests unitarios y de integración.

---

## 📄 Licencia
MIT — uso educativo.

## ✍️ Autor
Reinaldo José Loyo Sequera
