<script setup>
import { ref, onMounted, onUnmounted } from "vue"; // Add 'ref' here

//example components
import NavbarDefault from "../..//examples/navbars/NavbarDefault.vue";
import DefaultFooter from "../../examples/footers/FooterDefault.vue";
import Header from "../../examples/Header.vue";
import FilledInfoCard from "../../examples/cards/infoCards/FilledInfoCard.vue";

//Vue Material Kit 2 components
import MaterialSocialButton from "@/components/MaterialSocialButton.vue";

// sections
import PresentationCounter from "./Sections/PresentationCounter.vue";
import PresentationPages from "./Sections/PresentationPages.vue";
import PresentationExample from "./Sections/PresentationExample.vue";
import data from "./Sections/Data/designBlocksData";
import BuiltByDevelopers from "./Components/BuiltByDevelopers.vue";
import PresentationTestimonials from "./Sections/PresentationTestimonials.vue";
import PresentationInformation from "./Sections/PresentationInformation.vue";

//images
import vueMkHeader from "@/assets/img/header.jpg";
import wavesWhite from "@/assets/img/waves-white.svg";
import logoBootstrap from "@/assets/img/logos/bootstrap5.jpg";
import logoTailwind from "@/assets/img/logos/icon-tailwind.jpg";
import logoVue from "@/assets/img/logos/vue.jpg";
import logoAngular from "@/assets/img/logos/angular.jpg";
import logoReact from "@/assets/img/logos/react.jpg";
import logoSketch from "@/assets/img/logos/sketch.jpg";

//hooks
// Estado para controlar el modal
const showModal = ref(false);

// Mostrar el modal
const openModal = () => {
  showModal.value = true;
};

// Ocultar el modal
const closeModal = () => {
  showModal.value = false;
};

// Estilos iniciales de tu página
const body = document.getElementsByTagName("body")[0];
onMounted(() => {
  body.classList.add("presentation-page");
  body.classList.add("bg-gray-200");
});
onUnmounted(() => {
  body.classList.remove("presentation-page");
  body.classList.remove("bg-gray-200");
});
</script>

<template>
  <div class="container position-sticky z-index-sticky top-0">
    <div class="row">
      <div class="col-12">
        <NavbarDefault :sticky="true" />
      </div>
    </div>
  </div>
  <Header>
    <div
      class="page-header min-vh-75"
      :style="`background-image: url(${vueMkHeader})`"
      loading="lazy"
    >
      <div class="container">
        <div class="row">
          <div class="col-lg-7 text-center mx-auto position-relative">
            <h1
              class="text-white pt-3 mt-n5 me-2"
              :style="{ display: 'inline-block ' }"
            >
              Airdrum Project
            </h1>
            <p class="lead text-white px-5 mt-3" :style="{ fontWeight: '500' }">
              ¡Descubre una nueva forma de hacer música! Nuestra tecnología de
              baquetas inalámbricas para tocar batería te permite vivir la
              emoción de la percusión sin necesidad de un set físico. ¡Convierte
              cualquier espacio en tu escenario y lleva tu pasión por la música
              al siguiente nivel! 🎶🥁
            </p>
          </div>
        </div>
      </div>
    </div>
  </Header>

  <div class="card card-body blur shadow-blur mx-3 mx-md-4 mt-n6">
    <PresentationCounter />
    <PresentationInformation />
    <!-- <PresentationExample :data="data" />
    <PresentationPages /> -->
    <BuiltByDevelopers />

    <div class="container">
      <div class="row">
        <div class="col-lg-4">
          <FilledInfoCard
            class="p-4"
            :color="{ text: 'white', background: 'bg-gradient-success' }"
            :icon="{ component: 'flag', color: 'white' }"
            title="Comienza a Crear Ritmos"
            description="Explora las diversas formas de disfrutar nuestras baquetas inalámbricas y obtén los recursos necesarios para empezar a crear tu propia experiencia musical."
            :action="{
              label: { text: 'Let\'s start', color: 'white' },
            }"
          />
        </div>
        <div class="col-lg-4">
          <FilledInfoCard
            class="px-lg-1 mt-lg-0 mt-4 p-4"
            height="h-100"
            :icon="{ component: 'precision_manufacturing', color: 'success' }"
            title="Complementos"
            description="Descubre complementos inspiradores y obtén una visión general de las herramientas que utilizamos para mejorar la experiencia de Airdrum."
            :action="{
              label: { text: 'Read more' },
            }"
          />
        </div>
        <div class="col-lg-4">
          <FilledInfoCard
            class="px-lg-1 mt-lg-0 mt-4 p-4"
            :icon="{ component: 'receipt_long', color: 'success' }"
            title="Clases Utilitarias"
            description="Airdrum ofrece una variedad de elementos predefinidos. Para quienes buscan flexibilidad, hemos incluido numerosas clases utilitarias para personalizar tu experiencia."
            :action="{
              label: { text: 'Read more' },
            }"
          />
        </div>
      </div>
    </div>
    <!-- <PresentationTestimonials /> -->

    <div
      class="container-fluid mt-sm-5 border-radius-xl"
      :style="{
        background: 'linear-gradient(195deg, rgb(66, 66, 74), rgb(25, 25, 25))',
      }"
    >
      <div
        class="page-header py-6 py-md-5 my-sm-3 mb-3 border-radius-xl"
        :style="{
          backgroundImage: `url(${wavesWhite})`,
        }"
        loading="lazy"
      >
        <span class="mask bg-gradient-dark"></span>
        <div class="container">
          <div class="row">
            <div class="d-flex justify-content-center p-5">
              <div class="col-lg-8 ms-lg-5 text-center">
                <h3 class="text-white">
                  ¿Te apasiona la música y la tecnología?
                </h3>
                <p class="text-white text-md">
                  Si es así, ¡nuestras baquetas inalámbricas pueden ser tuyas!
                  Haz clic en el botón a continuación para obtener más
                  información sobre cómo puedes mejorar tu experiencia musical.
                  Ya sea que estés comenzando o buscando nuevas formas de tocar,
                  nuestras baquetas te permitirán llevar tu creatividad al
                  siguiente nivel.
                </p>

                <a
                  href="#"
                  class="btn btn-sm mb-0 bg-gradient-success px-5 py-3 mt-4"
                  @click.prevent="openModal"
                >Pruebalo ahora</a>

                <!-- Modal -->
                <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
                  <div class="modal-content">
                    <div class="modal-card">
                      <div class="modal-header">
                        <h2 class="modal-title">Suscripcion mensual</h2>
                        <p class="modal-price">10 Bs</p>
                      </div>
                      <div class="modal-body">
                        <p class="modal-description">
                          Con tu suscripcion mensual podras tener acceso a nuestro servicio de monitoreo de datos en tiempo real. Aprenderas a tocar aun mejor la bateria y mejorar ás tu técnica.
                        </p>
                      </div>
                      <div class="modal-footer">
                        <button class="btn-buy-now" @click="closeModal">Compra ahora</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <DefaultFooter />
</template>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter, .modal-fade-leave-to {
  opacity: 0;
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-in-out;
}

/* Modal Content */
.modal-content {
  background-color: #fff;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.4s ease-in-out;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Modal Card */
.modal-card {
  padding: 20px;
}

/* Modal Header */
.modal-header {
  text-align: center;
  margin-bottom: 15px;
}

.modal-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.modal-price {
  font-size: 22px;
  font-weight: 600;
  color: #2ecc71;
}

/* Modal Body */
.modal-body {
  text-align: center;
  font-size: 16px;
  color: #777;
  margin-bottom: 20px;
}

/* Modal Footer */
.modal-footer {
  text-align: center;
}

.btn-buy-now {
  background: linear-gradient(45deg, #2ecc71, #27ae60);
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 30px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-buy-now:hover {
  background: linear-gradient(45deg, #27ae60, #2ecc71);
}

@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

@keyframes slideIn {
  0% { transform: translateY(-50px); }
  100% { transform: translateY(0); }
}
</style>
