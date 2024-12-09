<script setup>
import DefaultCounterCard from "../../../examples/cards/counterCards/DefaultCounterCard.vue";
</script>

<template>
  <section class="pt-3 pb-4" id="count-stats">
    <div class="container">
      <div class="row">
        <div class="col-lg-9 z-index-2 border-radius-xl mx-auto py-3">
          <div class="row">
            <div class="col-md-4 position-relative">
              <DefaultCounterCard
                color="success"
                title="Prototipos Actuales"
                description="Lleva la experiencia de tocar la batería a cualquier lugar con nuestras baquetas inalámbricas, sin cables ni restricciones."
                :count="100"
                suffix="+"
                :duration="3000"
                divider="vertical"
              />
            </div>
            <div class="col-md-4 position-relative">
              <DefaultCounterCard
                color="success"
                title="Frecuencia de Respuesta"
                description="Disfruta de una respuesta ultra rápida para una experiencia musical sin retrasos. ¡Siente el ritmo como nunca antes!"
                :count="1"
                suffix="+"
                :duration="3000"
                divider="vertical"
              />
            </div>
            <div class="col-md-4">
              <DefaultCounterCard
                color="success"
                title="Facilidad de Uso"
                description="Configura tu baqueta inalámbrica en menos de 5 minutos y empieza a tocar. ¡Perfecto para principiantes y profesionales!"
                :count="5"
                :duration="3000"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
