<template>
  <div class="home-container">
    <header class="hero">
      <h1>Bienvenido a CEDICA</h1>
      <p>Promoviendo la inclusión social mediante la rehabilitación ecuestre.</p>
      <img src="../assets/images/imagen_cabalgata.jpg" alt="CEDICA" class="hero-image" />
    </header>

    <section class="about-us">
      <h2>¿Quiénes Somos?</h2>
      <div class="about-section" v-for="(content, index) in aboutContent" :key="index">
        <div :class="['about-text', { 'order-right': index % 2 === 1 }]">
          <p>{{ content.text }}</p>
        </div>
        <div :class="['about-image', { 'order-left': index % 2 === 1 }]">
          <img :src="content.image" :alt="content.alt" class="animated-image" />
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import terapia_caballo from '@/assets/images/terapia_caballo.jpg'
import equipo_profesional from '@/assets/images/equipo_profesional.jpg'
import equipo_trabajo from '@/assets/images/equipo_trabajo.jpeg'
import hipodromo from '@/assets/images/hipodromo.jpg'

export default {
  data() {
    return {
      aboutContent: [
        {
          text: `CEDICA (Centro de Equitación para Personas con Discapacidad y Carenciadas) es una Asociación Civil sin Fines de Lucro fundada en 1994 en la ciudad de La Plata. Nuestra misión es promover la inclusión social mediante la rehabilitación ecuestre.`,
          image: terapia_caballo,
          alt: 'Terapia con caballos',
        },
        {
          text: `Trabajamos con alumnos y alumnas que provienen de instituciones de menores, hospitales, centros de salud y barrios carenciados. Todas nuestras actividades son gratuitas y financiadas por diferentes instituciones.`,
          image: equipo_profesional,
          alt: 'Equipo profesional de CEDICA',
        },
        {
          text: `Nuestro equipo está compuesto por psicólogos, psicopedagogos, terapistas ocupacionales, profesores de educación especial y física, y más. Juntos ofrecemos un programa adaptado a cada persona.`,
          image: equipo_trabajo,
          alt: 'Equipo trabajando',
        },
        {
          text: `Funcionamos desde nuestras instalaciones en el Hipódromo de La Plata y en el Campo Arroyo San Juan. Ofrecemos becas de equitación y criamos caballos para terapia.`,
          image: hipodromo,
          alt: 'Instalaciones de CEDICA',
        },
      ],
    }
  },
}
</script>

<style scoped>

.hero {
  text-align: center;
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 3rem;
  color: var(--heading-color);
}

.hero p {
  font-size: 1.2rem;
  margin: 1rem 0;
  color: var(--text-color);
}

.hero-image {
  width: 100%;
  max-width: 600px;
  border-radius: 12px;
  margin-top: 1.5rem;
  transition: transform 0.3s ease-in-out;
}

.hero-image:hover {
  transform: scale(1.05);
}


.about-us {
  margin: 4rem 0;
}

.about-us h2 {
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 2rem;
  color: var(--heading-color);
}

.about-section {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.about-text {
  flex: 1;
  padding: 1rem;
}

.about-image {
  flex: 1;
  text-align: center;
}

.animated-image {
  width: 100%;
  max-width: 400px;
  border-radius: 12px;
  transition: transform 0.3s ease-in-out;
}

.animated-image:hover {
  transform: scale(1.05);
}


.order-right {
  order: 2;
}

.order-left {
  order: 1;
}


.gallery {
  margin: 4rem 0;
}

.gallery h2 {
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 2rem;
}

.gallery-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.gallery-item {
  text-align: center;
}

.gallery-image {
  width: 100%;
  border-radius: 8px;
  transition:
    transform 0.3s ease-in-out,
    box-shadow 0.3s ease-in-out;
}

.gallery-image:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .about-section {
    flex-direction: column;
    text-align: center;
  }

  .about-text, .about-image {
    order: 0; 
    flex: none; 
    padding: 0.5rem;
  }

  .animated-image {
    max-width: 100%; 
  }
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem; 
  }

  .hero p {
    font-size: 1rem; 
  }

  .hero-image {
    max-width: 100%; 
    margin-top: 1rem;
  }

  .about-us h2 {
    font-size: 1.8rem; 
  }

  .about-text {
    font-size: 1rem; 
  }
}
@media (max-width: 768px) {
  .gallery-grid {
    grid-template-columns: 1fr;
    gap: 1rem; 
  }

  .gallery-image {
    max-width: 100%;
  }
}
@media (max-width: 768px) {
  .home-container {
    padding: 1rem;
  }

  .about-us, .gallery {
    margin: 2rem 0;
  }
}
@media (max-width: 480px) {
  .hero h1 {
    font-size: 1.5rem;
  }

  .hero p {
    font-size: 0.9rem;
  }

  .about-text {
    font-size: 0.9rem;
  }

  .animated-image {
    max-width: 90%; 
  }
}

.animated-image, .gallery-image {
  cursor: pointer;
}

@media (max-width: 768px) {
  .animated-image:hover,
  .gallery-image:hover {
    transform: none; 
  }
}


</style>
