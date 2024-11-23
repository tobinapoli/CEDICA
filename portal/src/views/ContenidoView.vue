<script setup>
import ContenidoList from '@/components/ContenidoList.vue';
/**
 * Componente principal que contiene la lista de contenidos.
 * 
 * Este componente es el punto de entrada a la vista principal y contiene el componente `ContenidoList`,
 * que es responsable de mostrar la lista de contenidos (actividades y noticias).
 * Se puede utilizar para renderizar una vista donde se presenten los contenidos obtenidos
 * de la API o de un store de Vue/Pinia.
 */
</script>
<template>
    <main>
        <ContenidoList/>
    </main>
</template>