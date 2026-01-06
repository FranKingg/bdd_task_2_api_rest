# 📚 API de Gestión de Biblioteca

Proyecto desarrollado para la asignatura **Bases de Datos II – Ingeniería en Computación e Informática**  
Universidad de Magallanes (UMAG)

---

## 🧾 Descripción General

Este proyecto corresponde a una **API REST para la gestión de una biblioteca**, desarrollada utilizando **Litestar**, **SQLAlchemy** y **PostgreSQL**, siguiendo el patrón **Repositorio–Controlador**.  

La API permite administrar:
- Usuarios
- Libros
- Categorías
- Préstamos
- Reseñas

Además, implementa **autenticación JWT**, validaciones de negocio, relaciones complejas (many-to-many) y migraciones de base de datos con **Alembic**.

---

## 🎯 Objetivo del Proyecto

Aplicar conocimientos de:
- Desarrollo de APIs REST
- ORM con SQLAlchemy
- Migraciones de base de datos con Alembic
- Autenticación con JWT
- Uso de DTOs para control de datos
- Implementación de lógica de negocio en repositorios

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.13**
- **Litestar**
- **SQLAlchemy**
- **Alembic**
- **PostgreSQL**
- **Argon2** (hash de contraseñas)
- **JWT (OAuth2)**

---

## 🗂️ Estructura del Proyecto

```
bdd_2_api_rest/
├── app/
│   ├── controllers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── books.py
│   │   ├── categories.py
│   │   ├── loans.py
│   │   └── reviews.py
│   ├── repositories/
│   ├── models/
│   ├── dtos/
│   ├── security/
│   └── core/
├── migrations/
├── initial_data.sql
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## 🔐 Autenticación y Seguridad

- La API utiliza **JWT** para proteger los endpoints.
- El login se realiza mediante `/auth/login`.
- Las contraseñas se almacenan **hasheadas con Argon2**.
- Los endpoints protegidos requieren el header:
  ```
  Authorization: Bearer <token>
  ```

---

## 👤 Usuarios

### Campos implementados
- `username` (único)
- `fullname`
- `email` (único y validado)
- `phone`
- `address`
- `is_active` (por defecto `true`)
- `password` (hash Argon2)

### Validaciones
- Email con formato válido
- Email único
- `is_active` no puede ser modificado directamente por el usuario

---

## 📚 Libros

### Campos implementados
- `title`
- `author`
- `isbn`
- `pages`
- `published_year`
- `stock` (por defecto 1)
- `description`
- `language` (`es`, `en`, `fr`)
- `publisher`

### Validaciones
- `stock` > 0 al crear
- `stock` no puede ser negativo al actualizar
- Idioma restringido a códigos permitidos

---

## 🏷️ Categorías (Many-to-Many)

- Relación **muchos a muchos** entre libros y categorías
- Tabla intermedia `book_categories`
- CRUD completo de categorías
- Endpoint para obtener libros por categoría

---

## ⭐ Reseñas

### Campos
- `rating` (1 a 5)
- `comment`
- `review_date`
- Relación con `User` y `Book`

### Validaciones
- Rating obligatorio entre 1 y 5
- Reseñas asociadas correctamente a usuario y libro

---

## 📦 Préstamos

### Campos
- `loan_dt`
- `due_date` (calculado automáticamente: +14 días)
- `return_dt`
- `fine_amount` (Decimal, 2 decimales)
- `status` (`ACTIVE`, `RETURNED`, `OVERDUE`)

### Lógica de negocio
- Cálculo automático de fecha de vencimiento
- Cálculo de multa por atraso
- Cambio de estado al devolver un libro
- Obtención de préstamos activos
- Historial de préstamos por usuario

---

## 🧪 Datos Iniciales

Se incluye el archivo **`initial_data.sql`**, el cual carga:
- 5 categorías
- 10 libros
- 5 usuarios (contraseñas hasheadas)
- Préstamos activos, vencidos y devueltos
- Relaciones entre libros y categorías

---

## 🚀 Ejecución del Proyecto

### 1️⃣ Crear entorno e instalar dependencias
```bash
uv venv
uv pip install -r requirements.txt
```

### 2️⃣ Configurar variables de entorno
Crear archivo `.env`:
```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/litestart_db
JWT_SECRET=secret123
```

### 3️⃣ Ejecutar migraciones
```bash
uv run alembic upgrade head
```

### 4️⃣ Cargar datos iniciales
```bash
psql -U postgres -d litestart_db -f initial_data.sql
```

### 5️⃣ Levantar servidor
```bash
uv run litestar run
```

---

## 📖 Documentación de la API

- **Swagger UI**:  
  ```
  http://127.0.0.1:8000/schema/swagger
  ```
- **ReDoc**:  
  ```
  http://127.0.0.1:8000/schema/redoc
  ```

---

## ✅ Estado del Proyecto

✔ Todos los requisitos solicitados en la tarea fueron implementados  
✔ Migraciones funcionando correctamente  
✔ Validaciones de negocio aplicadas  
✔ Autenticación y autorización operativa  
✔ Datos iniciales incluidos  

---
