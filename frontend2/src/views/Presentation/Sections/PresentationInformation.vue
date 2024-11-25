<script setup>
import RotatingCard from "../../../examples/cards/rotatingCards/RotatingCard.vue";
import RotatingCardFront from "../../../examples/cards/rotatingCards/RotatingCardFront.vue";
import RotatingCardBack from "../../../examples/cards/rotatingCards/RotatingCardBack.vue";
import DefaultInfoCard from "../../../examples/cards/infoCards/DefaultInfoCard.vue";
</script>
<template>
  <section class="my-5 py-5">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-lg-4 ms-auto me-auto p-lg-4 mt-lg-0 mt-4">
          <RotatingCard>
            <RotatingCardFront
              image="https://plus.unsplash.com/premium_photo-1661299213170-6ca8f722f906?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              icon="touch_app"
              title="Siente la <br /> Música Inalámbrica"
              description="Con nuestras baquetas inalámbricas, experimenta la libertad de tocar sin restricciones y con total adaptabilidad al ritmo que desees."
            />

            <RotatingCardBack
            image="https://images.unsplash.com/photo-1498889444388-e67ea62c464b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1365&q=80"
              title="Descubre Más"
              description="Toca en cualquier lugar, sin cables, y ajusta la sensibilidad y los efectos de sonido para crear la experiencia musical perfecta para ti."
              :action="[{
                label: 'Explora nuestras características',
              }]"
            />
          </RotatingCard>
        </div>
        <div class="col-lg-6 ms-auto">
          <div class="row justify-content-start">
            <DefaultInfoCard
              icon="content_copy"
              title="Guía Completa"
              description="Desde la configuración inicial hasta el uso avanzado, nuestra documentación te guiará para sacar el máximo provecho a tu baqueta inalámbrica."
            />
            <DefaultInfoCard
              icon="flip_to_front"
              title="Adaptabilidad Total"
              description="Ajusta las baquetas a tu estilo de música. Nuestra tecnología te permite personalizar la experiencia según el género que prefieras."
            />
          </div>
          <div class="row justify-content-start mt-5">
            <DefaultInfoCard
              class="mt-3"
              icon="price_change"
              title="Ahorra Espacio y Dinero"
              description="Elimina la necesidad de equipos pesados y costosos. Con nuestras baquetas inalámbricas, solo necesitas lo esencial para tocar en cualquier momento."
            />
            <DefaultInfoCard
              class="mt-3"
              icon="devices"
              title="Totalmente Portátil"
              description="Lleva tus baquetas inalámbricas a donde quieras. Perfectas para ensayos, presentaciones en vivo o simplemente para practicar en casa."
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
