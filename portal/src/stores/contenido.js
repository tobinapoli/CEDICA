import { defineStore } from 'pinia'
import axios from 'axios'

/**
 * Store para gestionar contenidos y su paginación.
 * 
 * Este store se encarga de obtener los contenidos desde una API, gestionar el estado
 * de carga y error, y controlar la paginación para la visualización de los contenidos.
 */

export const useContenidosStore = defineStore('contenido', {
  state: () => ({
    contenidos: [],  // Lista de contenidos obtenidos desde la API
    loading: false, // Estado de carga (verdadero cuando se están obteniendo los contenidos)
    error: null, // Error si ocurre algún problema al obtener los contenidos
    pagination: { 
      page: 1, // Página actual
      perPage: 8, // Contenidos por página
      totalPages: 0, // Total de páginas
    },
  }),
  actions: {
    /**
     * Obtiene los contenidos desde la API y actualiza el estado.
     * 
     * Esta función realiza una solicitud a la API para obtener los contenidos de la página
     * indicada. Además, maneja los estados de carga y error y actualiza la paginación.
     * 
     * Por defecto se carga la pagina 1
     */
    async fetchContenidos(page = 1) {
      try {
        this.loading = true
        this.error = null

        // Actualiza el estado de la paginación con la nueva página
        this.pagination.page = page


        // Solicitud a la API para obtener los contenidos
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/contenido/`, {
          params: {
            page: this.pagination.page,
            perPage: this.pagination.perPage,
          },
        })
        
        // Actualiza los contenidos si la respuesta es válida
        if (response.data && response.data.data) {
          this.contenidos = response.data.data
        } else {
          this.contenidos = []
        }

        this.pagination.totalPages = response.data.totalPages // Total de páginas
      } catch (error) {
        this.error = 'Error al cargar el contenido'
      } finally {
        this.loading = false // Finaliza la carga, independientemente de si hubo error
      }
    },
  },
})
