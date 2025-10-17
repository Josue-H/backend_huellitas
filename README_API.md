# 🐾 API Huellitas - Documentación de Endpoints

Documentación completa de la API REST del sistema de gestión del Refugio Huellitas.

**Base URL:** `http://localhost:8000/api/`

---

## 📋 Tabla de Contenidos

1. [Autenticación](#autenticación)
2. [Mascotas](#mascotas)
3. [Noticias](#noticias)
4. [Historias de Éxito (Testimonios)](#historias-de-éxito-testimonios)
5. [Contacto](#contacto)
6. [Adopciones](#adopciones)
7. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🔐 Autenticación

### Login
```http
POST /api/authentication/login/
```

**Body:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "abc123...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@huellitas.org"
  }
}
```

### Logout
```http
POST /api/authentication/logout/
```

**Headers:**
```
Authorization: Token abc123...
```

---

## 🐶 Mascotas

### Listar todas las mascotas
```http
GET /api/pets/
```

**Query Parameters:**
- `species` - Filtrar por especie (dog, cat)
- `size` - Filtrar por tamaño (pequeño, mediano, grande)
- `status` - Filtrar por estado (available, in_process, adopted)
- `search` - Búsqueda por nombre
- `gender` - Filtrar por género (macho, hembra)

**Ejemplo:**
```http
GET /api/pets/?species=dog&size=mediano&status=available
```

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Daisy",
      "species": "dog",
      "species_display": "Perro",
      "breed": "Mestizo",
      "age_years": 2,
      "age_months": 3,
      "age_display": "2 años, 3 meses",
      "gender": "hembra",
      "gender_display": "Hembra",
      "size": "mediano",
      "size_display": "Mediano",
      "color": "Café",
      "description": "Perrita muy juguetona y cariñosa",
      "health_status": "healthy",
      "is_sterilized": true,
      "is_vaccinated": true,
      "status": "available",
      "status_display": "Disponible para adopción",
      "main_image": "http://localhost:8000/media/pets/daisy.jpg",
      "entry_date": "2024-10-01",
      "adoption_date": null,
      "is_active": true,
      "created_at": "2024-10-01T10:00:00Z"
    }
  ]
}
```

### Obtener mascota por ID
```http
GET /api/pets/{id}/
```

**Response:** (igual que el objeto individual de arriba)

### Mascotas disponibles
```http
GET /api/pets/available/
```

### Mascotas destacadas
```http
GET /api/pets/featured/
```

### Crear mascota (Admin)
```http
POST /api/pets/
```

**Headers:**
```
Authorization: Token abc123...
Content-Type: application/json
```

**Body:**
```json
{
  "name": "Rocky",
  "species": "dog",
  "breed": "Labrador",
  "age_years": 3,
  "age_months": 0,
  "gender": "macho",
  "size": "grande",
  "color": "Negro",
  "description": "Perro muy activo",
  "health_status": "healthy",
  "is_sterilized": true,
  "is_vaccinated": true
}
```

### Actualizar mascota (Admin)
```http
PUT /api/pets/{id}/
PATCH /api/pets/{id}/
```

### Eliminar mascota (Admin - Soft Delete)
```http
DELETE /api/pets/{id}/
```

---

## 📰 Noticias

### Listar noticias
```http
GET /api/content/news/
```

**Query Parameters:**
- `is_featured` - Filtrar destacadas (true/false)
- `search` - Búsqueda en título, resumen y contenido

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "title": "Jornada de Esterilización",
      "slug": "jornada-de-esterilizacion",
      "summary": "Realizamos 50 esterilizaciones gratuitas",
      "content": "El sábado pasado...",
      "featured_image": "http://localhost:8000/media/news/jornada.jpg",
      "is_featured": true,
      "published_date": "2024-10-10T15:00:00Z",
      "author": 1,
      "author_name": "Dortega",
      "is_active": true
    }
  ]
}
```

### Obtener noticia por ID o Slug
```http
GET /api/content/news/{id}/
GET /api/content/news/{slug}/
```

**Ejemplo:**
```http
GET /api/content/news/3/
GET /api/content/news/jornada-de-esterilizacion/
```

### Noticias destacadas
```http
GET /api/content/news/featured/
```

### Crear noticia (Admin)
```http
POST /api/content/news/
```

**Headers:**
```
Authorization: Token abc123...
Content-Type: multipart/form-data
```

**Body (Form Data):**
```
title: "Nueva noticia"
slug: "nueva-noticia"
summary: "Resumen de la noticia"
content: "Contenido completo..."
featured_image: [archivo]
is_featured: true
```

---

## 🎉 Historias de Éxito (Testimonios)

### Listar historias de éxito
```http
GET /api/content/success-stories/
```

**Response:**
```json
{
  "count": 4,
  "results": [
    {
      "id": 1,
      "title": "¡Una experiencia increíble!",
      "pet_name": "Rocky",
      "adopter_name": "Angela de Jesus",
      "story": "Adoptar a Rocky cambió mi vida...",
      "before_image": "http://localhost:8000/media/success_stories/before/rocky_before.jpg",
      "after_image": "http://localhost:8000/media/success_stories/after/rocky_after.jpg",
      "imagen": "http://localhost:8000/media/success_stories/after/rocky_after.jpg",
      "is_featured": true,
      "created_at": "2024-10-11T16:00:00Z"
    }
  ]
}
```

### Obtener historia por ID
```http
GET /api/content/success-stories/{id}/
```

### Historias destacadas
```http
GET /api/content/success-stories/featured/
```

### Crear historia (Admin)
```http
POST /api/content/success-stories/
```

---

## 📧 Contacto

### Enviar mensaje de contacto
```http
POST /api/contact/messages/
```

**Body:**
```json
{
  "full_name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "+502 1234-5678",
  "subject": "general",
  "message": "Me gustaría información sobre..."
}
```

**Opciones de `subject`:**
- `general` - Consulta general
- `volunteer` - Quiero ser voluntario
- `donation` - Donaciones
- `found_pet` - Encontré una mascota
- `lost_pet` - Perdí mi mascota
- `other` - Otro

**Response:**
```json
{
  "message": "Mensaje enviado exitosamente. Nos pondremos en contacto pronto.",
  "message_id": 2
}
```

### Listar mensajes (Admin)
```http
GET /api/contact/messages/
```

**Headers:**
```
Authorization: Token abc123...
```

### Actualizar estado del mensaje (Admin)
```http
PATCH /api/contact/messages/{id}/
```

**Body:**
```json
{
  "status": "resolved",
  "admin_response": "Hemos recibido tu mensaje..."
}
```

---

## 💝 Adopciones

### Enviar solicitud de adopción (Formulario PDF)
```http
POST /api/adoptions/simplified/
```

**Headers:**
```
Content-Type: multipart/form-data
```

**Body (Form Data):**
```
pet: 1
full_name: "María López"
pet_name_requested: "Daisy"
phone: "+502 5555-5555"
filled_form_pdf: [archivo PDF]
```

**Response:**
```json
{
  "message": "Solicitud enviada exitosamente. Nos pondremos en contacto pronto.",
  "application_id": 5
}
```

### Listar solicitudes de adopción (Admin)
```http
GET /api/adoptions/simplified/
```

**Headers:**
```
Authorization: Token abc123...
```

**Query Parameters:**
- `status` - Filtrar por estado (Recibida, En Revisión, Aprobada, Rechazada)
- `pet` - Filtrar por mascota (ID)

### Obtener solicitud por ID (Admin)
```http
GET /api/adoptions/simplified/{id}/
```

### Actualizar estado de solicitud (Admin)
```http
PATCH /api/adoptions/simplified/{id}/
```

**Body:**
```json
{
  "status": "Aprobada",
  "admin_notes": "Cumple con todos los requisitos"
}
```

### Descargar formulario de adopción en blanco
```http
GET /api/adoptions/download-form/
```

**Response:** Archivo PDF

---

## ❓ Preguntas Frecuentes

### Listar FAQs
```http
GET /api/content/faqs/
```

**Query Parameters:**
- `category` - Filtrar por categoría (adoption, care, donation, volunteer, general)

**Response:**
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "question": "¿Cuál es el proceso de adopción?",
      "answer": "El proceso incluye...",
      "category": "adoption",
      "category_display": "Adopción",
      "order": 1,
      "is_active": true
    }
  ]
}
```

### FAQs agrupados por categoría
```http
GET /api/content/faqs/by_category/
```

**Response:**
```json
{
  "Adopción": [
    {
      "id": 1,
      "question": "¿Cuál es el proceso?",
      "answer": "..."
    }
  ],
  "Cuidados": [
    {
      "id": 2,
      "question": "¿Qué vacunas necesita?",
      "answer": "..."
    }
  ]
}
```

---

## 🔧 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado exitosamente |
| 204 | No Content - Eliminación exitosa |
| 400 | Bad Request - Error en los datos enviados |
| 401 | Unauthorized - No autenticado |
| 403 | Forbidden - No tiene permisos |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

---

## 📝 Notas Importantes

### Autenticación
- Los endpoints marcados con **(Admin)** requieren autenticación
- Usar header: `Authorization: Token {tu_token}`

### Paginación
- La mayoría de endpoints de listado usan paginación
- Por defecto: 10-25 resultados por página
- Usar `?page=2` para la siguiente página

### Archivos
- Tamaño máximo de imágenes: 5MB
- Tamaño máximo de PDFs: 10MB
- Formatos aceptados:
  - Imágenes: JPG, PNG, WEBP
  - Documentos: PDF

### CORS
- Configurado para permitir requests desde `http://localhost:5173`
- En producción, actualizar en `settings.py`

---

## 🚀 Ejemplos de Uso con JavaScript

### Obtener mascotas disponibles
```javascript
const response = await fetch('http://localhost:8000/api/pets/available/');
const data = await response.json();
console.log(data);
```

### Enviar mensaje de contacto
```javascript
const response = await fetch('http://localhost:8000/api/contact/messages/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    full_name: "Juan Pérez",
    email: "juan@example.com",
    phone: "+502 1234-5678",
    subject: "general",
    message: "Hola, me gustaría..."
  })
});
const result = await response.json();
```

### Enviar solicitud de adopción con PDF
```javascript
const formData = new FormData();
formData.append('pet', 1);
formData.append('full_name', 'María López');
formData.append('pet_name_requested', 'Daisy');
formData.append('phone', '+502 5555-5555');
formData.append('filled_form_pdf', pdfFile); // File object

const response = await fetch('http://localhost:8000/api/adoptions/simplified/', {
  method: 'POST',
  body: formData
});
const result = await response.json();
```

---

## 📞 Contacto y Soporte

Para más información o reportar problemas:
- **Email:** dev@huellitas.org
- **GitHub:** [Repositorio del proyecto]

---

**Versión:** 1.0.0  
**Última actualización:** Octubre 2024  
**Desarrollado con ❤️ para Refugio Huellitas** 🐾
