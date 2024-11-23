<script setup>
import { useContenidosStore } from '@/stores/contenido'
import { storeToRefs } from 'pinia'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

/**
 * Componente para mostrar el detalle de un contenido específico.
 * 
 * Este componente obtiene los detalles de un contenido seleccionado desde una lista de contenidos,
 * mostrando su título, copete (descripción corta), contenido principal y el autor. También maneja 
 * los estados de carga y error mientras se obtiene la información.
 */

const store = useContenidosStore()
const { contenidos, loading, error } = storeToRefs(store)

const route = useRoute()
const contenido = ref(null)


/**
 * Función para obtener el contenido seleccionado desde la lista de contenidos.
 * 
 * Si no se ha cargado previamente la lista de contenidos, la función realiza una solicitud para obtenerla.
 * Luego, busca el contenido específico usando el `id` pasado en la ruta y lo asigna a la variable `contenido`.
 */
const fetchContenido = async () => {
  try {
    if (!contenidos.value.length) {
      await store.fetchContenidos(1); 
    }
    contenido.value = contenidos.value.find((item) => item.id === parseInt(route.params.id));
  } catch (err) {
    console.error('Error fetching contenido:', err);
  }
};

/**
 * Llama a la función `fetchContenido` cuando el componente se monta.
 */
onMounted(() => {
  fetchContenido()
})
</script>

<template>
  <div class="contenido-container">
    <!-- Título centrado -->
    <h1 v-if="!loading && contenido" class="contenido-titulo" v-html="contenido.titulo"></h1>

    <!-- Copete con breve descripción -->
    <p v-if="!loading && contenido" class="contenido-copete" v-html="contenido.copete"></p>

    <!-- Contenido principal -->
    <div
      v-if="!loading && contenido"
      class="contenido-principal"
      v-html="contenido.contenido"
    ></div>

    <!-- Botón para volver -->
    <div v-if="!loading" class="contenido-boton">
      <router-link to="/contenido" class="boton-volver">Volver a la lista</router-link>
    </div>

    <!-- Autor como pie de página -->
    <footer v-if="!loading && contenido" class="contenido-autor">
      Publicado por: {{ contenido.autor_email }}
    </footer>

    <!-- Mensajes de carga o error -->
    <p v-if="loading" class="contenido-cargando">Cargando contenido...</p>
    <p v-if="error" class="contenido-error">Error: {{ error }}</p>
  </div>
</template>

<style scoped>
/* Contenedor principal */
.contenido-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Título */
.contenido-titulo {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

/* Copete */
.contenido-copete {
  text-align: center;
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 30px;
  font-style: italic;
}

/* Contenido principal */
.contenido-principal {
  font-size: 1rem;
  line-height: 1.6;
  color: #444;
  margin-bottom: 40px;
  text-align: justify;
}

/* Pie de página con autor */
.contenido-autor {
  text-align: right;
  font-size: 0.9rem;
  color: #666;
  border-top: 1px solid #ddd;
  padding-top: 10px;
}

/* Mensajes de estado */
.contenido-cargando,
.contenido-error {
  text-align: center;
  font-size: 1rem;
  color: #888;
  margin-top: 20px;
}
</style>
