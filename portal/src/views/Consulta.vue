<template>
  <div class="consulta">
    <h1>Contáctanos</h1>
    <form @submit.prevent="onSubmit">
      <div>
        <label for="nombre">Nombre completo:</label>
        <input type="text" id="nombre" v-model="form.nombrecompleto" required />
      </div>
      <div>
        <label for="email">Correo electrónico:</label>
        <input
          type="email"
          id="email"
          v-model="form.correo"
          required
          pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
        />
      </div>
      <div>
        <label for="mensaje">Mensaje:</label>
        <textarea id="mensaje" v-model="form.mensaje" required></textarea>
      </div>
      <!-- Captcha Component -->
      <Captcha ref="captchaRef" :site-key="siteKey" @verify="onCaptchaVerify" />
      <button type="submit" :disabled="!captchaVerified">Enviar</button>
    </form>
  </div>
</template>

<script>
import { useConsultasStore } from '@/stores/consultas'
import Captcha from '@/components/Captcha.vue'

export default {
  components: { Captcha },
  data() {
    return {
      form: {
        nombrecompleto: '',
        correo: '',
        mensaje: '',
      },
      captchaVerified: false,
      recaptchaToken: null,
      siteKey: 'captchaKey' // Reemplaza con tu clave de sitio de reCAPTCHA,
    }
  },
  methods: {
    async onSubmit() {
      const consultasStore = useConsultasStore()
      const formData = {
        nombrecompleto: this.form.nombrecompleto,
        correo: this.form.correo,
        mensaje: this.form.mensaje,
      }
      console.log('Datos antes de enviar:', formData)
      console.log('Recaptcha Token antes de enviar:', this.recaptchaToken) // Verifica el valor del token

      if (!this.recaptchaToken) {
        alert('Por favor, verifica el reCAPTCHA antes de enviar.')
        return // Si no hay token, no envíes la consulta
      }
      try {
        await consultasStore.submitConsulta(formData, this.recaptchaToken)
        alert('Consulta enviada exitosamente.')
        this.resetForm()
      } catch (error) {
        alert('Error al enviar la consulta.')
      }
    },
    resetForm() {
      // Restablecer los valores del formulario a los valores iniciales
      this.form = {
        nombrecompleto: '',
        correo: '',
        mensaje: '',
      }
      // Opcional: restablecer otros valores como el estado del captcha
      this.captchaVerified = false
      this.recaptchaToken = null
      if (this.$refs.captchaRef) {
        this.$refs.captchaRef.resetCaptcha()
      }
    },
    onCaptchaVerify(isVerified, token) {
      console.log('Captcha Verificado:', isVerified)
      this.captchaVerified = isVerified
      this.recaptchaToken = token
    },
  },
}
</script>

<style scoped>
form {
  width: 100%;
  max-width: 500px;
  margin: auto;
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

form div {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input,
textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus,
textarea:focus {
  border-color: #007acc;
  outline: none;
}

button {
  background: #007acc;
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

button:disabled {
  background: #ccc;
}

button:hover {
  background: #005b99;
}
</style>
