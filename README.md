<h1 align="center">
  CEDICA Project
</h1>

<br/>
<br/>

## 📋 **Project Details**

- **Project Name**: Software Project 2024 - Integrative Work (TI)
- **Main Technologies**:
  - **Python** (Flask for backend)
  - **Vue.js** (Frontend for the public portal)
  - **PostgreSQL** (Database)
  - **HTML5, CSS3, JavaScript** (User interface)

<br/>
<br/>

## 📝 **Project Description**

The project involves the development of a **Web Application** for the **Center for Equine Therapy for People with Disabilities and Underprivileged Individuals (CEDICA)**, a non-profit civil association that uses horse-assisted therapies to improve the quality of life for people with disabilities.

The application is designed to manage information about **Riders and Amazons (R&A)**, **team professionals**, **horses**, and **payment and billing records**. Additionally, it includes a **public portal** to showcase the services offered by the institution.

<br/>

## 🛠️ **Key Features**

### **Private Application (Flask)**
- **User Module**: CRUD for users, role and permission management.
- **Team Module**: Employee registration, associated documentation, and payment management.
- **R&A Module**: Management of rider and amazon records, supplementary documentation, and billing records.
- **Equestrian Module**: Horse management, associated documentation, and trainer assignments.
- **Payment and Billing Records**: Recording financial transactions related to employees and R&A.
- **Content Management Module**: Management of publications for the public portal (articles, news, events).
- **Reports Module**: Visualization of statistics and charts about institutional data.
- **Contact Module**: Management of inquiries received from the public portal.
- **Google Authentication**: User registration and authentication via Google.

### **Public Portal (Vue.js)**
- **Home**: General information about the institution and its activities.
- **Contact**: Form to send inquiries to the CEDICA team.
- **Activities and News**: Display of publications and events loaded from the private application.

<br/>

## 📊 **Project Structure**

- **Backend**: Developed in Python with Flask. Includes business logic, REST API, and connection to the PostgreSQL database.
- **Frontend**: Developed in Vue.js for the public portal. Interacts with the backend via an API.
- **Database**: PostgreSQL to store all application data.
- **Authentication**: Login and session management system implemented from scratch (without external libraries like Flask-Login).

<br/>

<h2>📂 Installation and Usage</h2>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3.12 or higher.</li>
  <li>Node.js (for the Vue.js frontend).</li>
  <li>PostgreSQL 16.</li>
  <li>Git (to clone the repository).</li>
</ul>

<h3>Installation Steps</h3>

<ol>
  <li>
    <strong>Clone the repository:</strong>
    <pre><code>git clone https://github.com/tobinapoli/CEDICA.git
cd CEDICA</code></pre>
  </li>

  <li>
    <strong>Set up the virtual environment (Python):</strong>
    <pre><code>python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate</code></pre>
  </li>

  <li>
    <strong>Install backend dependencies:</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>

  <li>
    <strong>Set up the database:</strong>
    <ul>
      <li>Create a database in PostgreSQL.</li>
      <li>Configure credentials in the <code>config.py</code> file.</li>
      <li>Run migrations:
        <pre><code>flask db upgrade</code></pre>
      </li>
    </ul>
  </li>

  <li>
    <strong>Install frontend dependencies:</strong>
    <pre><code>cd portal
npm install</code></pre>
  </li>

  <li>
    <strong>Run the application:</strong>
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
    <strong>Access the application:</strong>
    <ul>
      <li><strong>Private Application:</strong> <code>http://localhost:5000</code></li>
      <li><strong>Public Portal:</strong> <code>http://localhost:8080</code></li>
    </ul>
  </li>
</ol>
