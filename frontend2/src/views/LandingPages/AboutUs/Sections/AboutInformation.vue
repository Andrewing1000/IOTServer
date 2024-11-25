<script setup>
// Componentes de ejemplo
import DefaultInfoCard from "../../../../examples/cards/infoCards/DefaultInfoCard.vue";
import CenteredBlogCard from "../../../../examples/cards/blogCards/CenteredBlogCard.vue";
</script>

<template>
  <section class="py-7">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-lg-6">
          <div class="row justify-content-start">
            <DefaultInfoCard
              color="info"
              icon="public"
              title="Plataforma totalmente integrada"
              description="Airdrum conecta innovaciones tecnológicas para ofrecerte una experiencia musical única y accesible desde cualquier lugar."
            />
            <DefaultInfoCard
              color="info"
              icon="payments"
              title="Funcionalidad de pagos"
              description="Airdrum permite a los usuarios realizar pagos dentro de la plataforma para acceder a contenido premium, clases y más."
            />
          </div>
          <div class="row justify-content-start mt-4">
            <DefaultInfoCard
              color="info"
              icon="apps"
              title="Componentes preconstruidos"
              description="La plataforma Airdrum ofrece una serie de componentes fáciles de usar que te permiten crear y personalizar tu experiencia musical."
            />
            <DefaultInfoCard
              color="info"
              icon="3p"
              title="Plataforma mejorada"
              description="Airdrum está en constante evolución, integrando nuevas herramientas y funciones para mejorar la experiencia del usuario."
            />
          </div>
        </div>
        <div class="col-lg-4 ms-auto mt-lg-0 mt-6">
          <CenteredBlogCard
            image="https://www.musisol.com/blog/wp-content/uploads/2021/03/partes-de-una-bateria-min.jpg"
            title="Descubre más sobre Airdrum"
            description="Explora las posibilidades que Airdrum ofrece para mejorar tu experiencia musical, desde crear ritmos hasta compartirlos con otros usuarios."
          />
        </div>
      </div>
    </div>
  </section>
</template>
