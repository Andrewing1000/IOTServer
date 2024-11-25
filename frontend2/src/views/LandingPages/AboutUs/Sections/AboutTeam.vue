<script setup>
// example component
import HorizontalTeamCard from "@/examples/cards/teamCards/HorizontalTeamCard.vue";

// images
import emma from "@/assets/img/team-5.jpg";
import william from "@/assets/img/fondoAIRDRUM_usuario.avif";
import ivana from "@/assets/img/ivana-squares.jpg";
import marquez from "@/assets/img/ivana-square.jpg";
</script>

<template>
  <section class="pb-5 position-relative bg-gradient-dark mx-n3">
    <div class="container">
      <div class="row">
        <div class="col-md-8 text-start mb-5 mt-5">
          <h3 class="text-white z-index-1 position-relative">
            Nuestro equipo de trabajo:
          </h3>
          <p class="text-white opacity-8 mb-0">
            Conoce a las personas que hacen posible Airdrum. Un grupo de trabajo enfocado en brindarte la mejor experiencia musical.
          </p>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-6 col-12">
          <HorizontalTeamCard
            class="mt-4"
            :image="william"
            :profile="{ name: 'Luis Angel Huanca', link: 'javascript:;' }"
            :position="{ label: 'UI Designer', color: 'success' }"
            description="Diseñador frontend con mucha experiencia en la creacion de interfaces "
          />
        </div>
        <div class="col-lg-6 col-12">
          <HorizontalTeamCard
            class="mt-lg-4 mt-5"
            :image="william"
            :profile="{ name: 'Rodrigo Camilo Mendez Gallardo', link: 'javascript:;' }"
            :position="{ label: 'Desarrolador Fronted', color: 'success' }"
            description="Programador enfocado en la creacion de interfaces"
          />
        </div>
      </div>
      <div class="row mt-4">
        <div class="col-lg-6 col-12">
          <HorizontalTeamCard
            class="mt-4 z-index-2"
            :image="william"
            :profile="{ name: 'Alex Quino Miranda', link: 'javascript:;' }"
            :position="{ label: 'Desarrolador Fronted', color: 'success' }"
            description="Experto en desarrolador fronted con mucha experiencia en la creacion de interfaces"
          />
        </div>
        <div class="col-lg-6 col-12">
          <HorizontalTeamCard
            class="mt-lg-4 mt-5 z-index-2"
            :image="william"
            :profile="{ name: 'Andres Hinojosa', link: 'javascript:;' }"
            :position="{ label: 'JS Developer', color: 'success' }"
            description="Desarrolador frontend con mucha experiencia en la creacion de interfaces"
          />
          
        </div>
        <div class="col-lg-6 col-12">
          <HorizontalTeamCard
            class="mt-4 z-index-2"
            :image="william"
            :profile="{ name: 'Santiago Machicado', link: 'javascript:;' }"
            :position="{ label: 'Desarrolador Backenb', color: 'success' }"
            description="Desarrolador backend con mucha experiencia en la creacion de interfaces"
          />
        </div>
      </div>
    </div>
  </section>
</template>
