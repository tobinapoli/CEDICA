<h1 align="center">
  Proyecto CEDICA
</h1>

<br/>
<br/>


## 📋 **Detalles del Proyecto**

- **Nombre del Proyecto**: Proyecto de Software 2024 - Trabajo Integrador (TI)
- **Tecnologías Principales**:
  -  **Python** (Flask para el backend)
  -  **Vue.js** (Frontend para el portal público)
  -  **PostgreSQL** (Base de datos)
  -  **HTML5, CSS3, JavaScript** (Interfaz de usuario)

<br/>
<br/>

## 📝 **Descripción del Proyecto**

El proyecto consiste en el desarrollo de una **Aplicación Web** para el **Centro de Equitación para Personas con Discapacidad y Carenciadas (CEDICA)**, una asociación civil sin fines de lucro que utiliza terapias asistidas con caballos para mejorar la calidad de vida de personas con discapacidad.

La aplicación está diseñada para gestionar la información de los **Jinetes y Amazonas (J&A)**, los **profesionales del equipo**, los **caballos**, y los **registros de pagos y cobros**. Además, cuenta con un **portal público** para mostrar los servicios ofrecidos por la institución.

<br/>

## 🛠️ **Funcionalidades Principales**

### **Aplicación Privada (Flask)**
- **Módulo de Usuarios**: CRUD de usuarios, gestión de roles y permisos.
- **Módulo de Equipo**: Registro de empleados, documentación asociada y gestión de pagos.
- **Módulo J&A**: Gestión de legajos de jinetes y amazonas, documentación complementaria y registros de cobros.
- **Módulo Ecuestre**: Gestión de caballos, documentación asociada y asignación de entrenadores.
- **Registro de Pagos y Cobros**: Registro de transacciones financieras relacionadas con empleados y J&A.
- **Módulo de Administración de Contenido**: Gestión de publicaciones para el portal público (artículos, noticias, eventos).
- **Módulo de Reportes**: Visualización de estadísticas y gráficos sobre datos de la institución.
- **Módulo de Contacto**: Gestión de consultas recibidas desde el portal público.
- **Autenticación con Google**: Registro y autenticación de usuarios mediante Google.

### **Portal Público (Vue.js)**
- **Home**: Información general sobre la institución y sus actividades.
- **Contacto**: Formulario para enviar consultas al equipo de CEDICA.
- **Actividades y Noticias**: Visualización de publicaciones y eventos cargados desde la aplicación privada.
<br/>


<br/>

## 📊 **Estructura del Proyecto**

- **Backend**: Desarrollado en Python con Flask. Incluye la lógica de negocio, la API REST y la conexión con la base de datos PostgreSQL.
- **Frontend**: Desarrollado en Vue.js para el portal público. Interactúa con el backend mediante una API.
- **Base de Datos**: PostgreSQL para almacenar toda la información de la aplicación.
- **Autenticación**: Sistema de login y manejo de sesiones implementado desde cero (sin librerías externas como Flask-Login).

<br/>

<h2>📂 Instalación y Uso</h2>

<h3>Requisitos Previos</h3>
<ul>
  <li>Python 3.12 o superior.</li>
  <li>Node.js (para el frontend con Vue.js).</li>
  <li>PostgreSQL 16.</li>
  <li>Git (para clonar el repositorio).</li>
</ul>

<h3>Pasos para la Instalación</h3>

<ol>
  <li>
    <strong>Clonar el repositorio:</strong>
    <pre><code>git clone https://github.com/tobinapoli/CEDICA.git
cd CEDICA</code></pre>
  </li>

  <li>
    <strong>Configurar el entorno virtual (Python):</strong>
    <pre><code>python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate</code></pre>
  </li>

  <li>
    <strong>Instalar dependencias del backend:</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>

  <li>
    <strong>Configurar la base de datos:</strong>
    <ul>
      <li>Crear una base de datos en PostgreSQL.</li>
      <li>Configurar las credenciales en el archivo <code>config.py</code>.</li>
      <li>Ejecutar las migraciones:
        <pre><code>flask db upgrade</code></pre>
      </li>
    </ul>
  </li>

  <li>
    <strong>Instalar dependencias del frontend:</strong>
    <pre><code>cd portal
npm install</code></pre>
  </li>

  <li>
    <strong>Ejecutar la aplicación:</strong>
    <ul>
      <li><strong>Backend (Flask):</strong>
        <pre><code>flask run </code></pre>
      </li>
      <li><strong>Frontend (Vue.js):</strong>
        <pre><code>npm run dev</code></pre>
      </li>
    </ul>
  </li>

  <li>
    <strong>Acceder a la aplicación:</strong>
    <ul>
      <li><strong>Aplicación Privada:</strong> <code>http://localhost:5000</code></li>
      <li><strong>Portal Público:</strong> <code>http://localhost:8080</code></li>
    </ul>
  </li>
</ol>
