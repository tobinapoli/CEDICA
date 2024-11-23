<script setup>

import { useContenidosStore } from '@/stores/contenido'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'

const store = useContenidosStore()
const { contenidos, loading, error, pagination } = storeToRefs(store)

/**
 * Función que obtiene los contenidos del store.
 * 
 * Esta función se encarga de llamar al método `fetchContenidos` del store,
 * pasando el número de página que se necesita cargar.
 */
const fetchContenidos = async (page) => {
  await store.fetchContenidos(page);
};


/**
 * Se ejecuta cuando el componente se monta en el DOM.
 * 
 * Si no hay contenidos cargados, se solicita la carga de la primera página.
 */
onMounted(() => {
  if (!contenidos.value.length) {
    fetchContenidos()
  }
})
</script>

<template>
  <div class="contenidos-container">
    <h1>Actividades y Noticias</h1>
    <p v-if="loading">Cargando...</p>
    <p v-if="error">Error: {{ error }}</p>

    <div v-if="!loading && contenidos.length" class="contenido-grid">
      <div v-for="contenido in contenidos" :key="contenido.id" class="contenido-card">
        <!-- Fecha de publicación -->
        <p class="contenido-fecha">{{ contenido.fecha_publicacion }}</p>
        <!-- Título -->
        <h2 class="contenido-titulo" v-html="contenido.titulo"></h2>
        <!-- Copete -->
        <p class="contenido-copete" v-html="contenido.copete"></p>
        <!-- Autor -->
        <p class="contenido-autor">Publicado por: {{ contenido.autor_email }}</p>
        <!-- Enlace -->
        <router-link
          :to="{ name: 'show_contenido', params: { id: contenido.id } }"
          class="contenido-link"
        >
          Ver más
        </router-link>
      </div>
    </div>

    <div v-if="!loading && pagination.totalPages > 1" class="pagination">
      <button
        class="pagination-btn"
        :disabled="pagination.page === 1"
        @click="fetchContenidos(pagination.page - 1)"
      >
        Anterior
      </button>
      <span class="pagination-info">
        Página {{ pagination.page }} de {{ pagination.totalPages }}
      </span>
      <button
        class="pagination-btn"
        :disabled="pagination.page === pagination.totalPages"
        @click="fetchContenidos(pagination.page + 1)"
      >
        Siguiente
      </button>
    </div>

    <div v-else-if="pagination.totalPages === 1" class="pagination">
      <button class="pagination-btn" disabled>Anterior</button>
      <span class="pagination-info">Página 1</span>
      <button class="pagination-btn" disabled>Siguiente</button>
    </div>
  </div>
</template>

<style scoped>

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  gap: 1rem;
}

/* Botón de paginación */
.pagination-btn {
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.pagination-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.pagination-btn:hover:not(:disabled) {
  background: var(--secondary-color);
}

/* Información de la paginación */
.pagination-info {
  font-size: 1rem;
  color: var(--text-color);
}
.contenidos-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background: var(--background-color);
}

/* Grid contenedor para las cards */
.contenido-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* Ajuste automático */
  gap: 1.5rem; /* Espacio entre cards */
  margin-top: 2rem;
}

/* Cada card de contenido */
.contenido-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: transform 0.2s ease-in-out;
  height: 350px; /* Altura fija para la tarjeta */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden; /* Evita que el contenido se desborde */
}

/* Fecha */
.contenido-fecha {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

/* Título */
.contenido-titulo {
  font-size: 1.5rem;
  color: var(--heading-color);
  margin-bottom: 1rem;
  overflow: hidden; /* Para evitar desbordamientos de texto */
  text-overflow: ellipsis; /* Agregar puntos suspensivos si el texto es muy largo */
  white-space: nowrap; /* Evitar que el texto se divida en varias líneas */
}

/* Copete */
.contenido-copete {
  font-size: 1rem;
  color: var(--text-color);
  margin-bottom: 1.5rem;
  text-align: left;
  overflow: hidden; /* Evitar que el texto se desborde */
  text-overflow: ellipsis; /* Puntos suspensivos si el copete es largo */
  display: -webkit-box;
  -webkit-line-clamp: 3; /* Limitar a 3 líneas */
  -webkit-box-orient: vertical;
}

/* Autor */
.contenido-autor {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 1rem;
  overflow: hidden;
}

/* Enlace para ver más */
.contenido-link {
  display: inline-block;
  background: var(--primary-color);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.9rem;
  transition: background 0.3s ease;
}

.contenido-link:hover {
  background: var(--secondary-color);
}
</style>
