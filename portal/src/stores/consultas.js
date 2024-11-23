import { defineStore } from "pinia";
import axios from "axios";

export const useConsultasStore = defineStore("consultas", {
  state: () => ({
    consultas: [],
  }),
  actions: {
    async submitConsulta(consultaData, recaptchaToken) {
      try {
        console.log("Datos recibidos en el store:", consultaData); 
        console.log("nombrecompleto:", consultaData.nombrecompleto);
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/contacto/`, {
          nombrecompleto: consultaData.nombrecompleto,
          correo: consultaData.correo,
          mensaje: consultaData.mensaje,
          recaptchaToken: recaptchaToken,  
        });
        console.log("Consulta enviada exitosamente:", response.data);
      } catch (error) {
        console.error("Error al enviar consulta:", error);
        throw error;
      }
    },
  },
});
