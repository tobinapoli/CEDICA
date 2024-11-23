<template>
  <div>
    <div
      id="captcha-container"
      class="g-recaptcha"
      :data-sitekey="siteKey"
      :data-callback="onVerify"
    ></div>
  </div>
</template>

<script>
export default {
  props: ["siteKey"],
  methods: {
    loadCaptchaScript() {
      // Carga el script de reCAPTCHA si no está cargado
      if (!document.getElementById("recaptcha-script")) {
        const script = document.createElement("script");
        script.id = "recaptcha-script";
        script.src = "https://www.google.com/recaptcha/api.js";
        script.async = true;
        script.defer = true;
        script.onload = this.initializeCaptcha;
        document.body.appendChild(script);
      } else {
        this.initializeCaptcha();
      }
    },
    initializeCaptcha() {
      // Inicializa reCAPTCHA si el script ya está cargado
      if (window.grecaptcha) {
        window.grecaptcha.render("captcha-container", {
          sitekey: this.siteKey,
          callback: this.onVerify,
        });
      } else {
        console.error("Error: reCAPTCHA no está disponible.");
      }
    },
    resetCaptcha() {
      if (window.grecaptcha) {
        window.grecaptcha.reset();
      }
    },
    onVerify(token) {
      // Emite el evento al componente principal
      this.$emit("verify", true, token);
    },
  },
  mounted() {
    // Carga el script de reCAPTCHA al montar el componente
    this.loadCaptchaScript();
  },
};
</script>
