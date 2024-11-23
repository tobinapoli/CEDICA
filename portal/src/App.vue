<script setup>
import { ref } from 'vue';
import { RouterLink, RouterView } from 'vue-router';

const isMenuOpen = ref(false);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};
</script>

<template>
  <header class="navbar">

    <img alt="Vue logo" src="\favicon.png" class="logo" width="50" height="50" />

    <button class="menu-toggle" @click="toggleMenu">
      ☰
    </button>

    <nav class="navbar-links" :class="{ 'open': isMenuOpen }">
      
      <RouterLink to="/" class="btn-nav" @click="isMenuOpen = false">Inicio</RouterLink>
      <RouterLink to="/contenido" class="btn-nav" @click="isMenuOpen = false">Actividades y Noticias</RouterLink>
      <RouterLink to="/consulta" class="btn-nav" @click="isMenuOpen = false">Consulta</RouterLink>
    </nav>
  </header>

  <main class="content">
    <RouterView />
  </main>
</template>

<style scoped>

.navbar {
  display: flex;
  flex-direction: row;
  justify-content: space-between; 
  background-color: lightblue;
  color: black;
  padding: 0.5rem 1.5rem;
  box-shadow: 0px 10px 6px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  transition: height 0.3s ease-in-out;
}

.navbar-links {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;  
  gap: 2rem;
  width: 100%; 
}

.navbar-links.open {
  display: flex;
  flex-direction: column;
  max-height: 200px;
  transition: max-height 0.3s ease-in-out;
}

.menu-toggle {
  display: none;
}

.btn-nav {
  text-decoration: none;
  color: black;
  font-weight: bold;
  padding: 0.5rem 2rem;  
  border-radius: 5px;
  transition: background-color 0.2s ease;
}

.btn-nav:hover {
  background-color: aliceblue;
}


@media (max-width: 600px) {

  .menu-toggle {
    display: block;
    position: absolute;  
    right: 1rem;  
    top: 1rem;  
    font-size: 1.5rem;  
  }

  .navbar-links {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-height: 0;
    overflow: hidden;  
    transition: max-height 0.3s ease-in-out;
  }

  
  .navbar-links.open {
    max-height: 300px; 
  }

  
  .btn-nav {
    text-align: center;
    width: 100%;
    padding: 1rem;
  }
}

@media (min-width: 601px) {
 
  .navbar-links {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;  
    gap: 2rem;
  }

  .menu-toggle {
    display: none;  
  }
}

.content {
  margin-top: 60px;
  padding: 1.5rem;
  text-align: center;
}

</style>
