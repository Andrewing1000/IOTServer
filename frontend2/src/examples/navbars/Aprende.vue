<template>
    <div id="aprende-page">
      <!-- Hero Section -->
      <section id="hero">
        <div class="hero-content">
          <h1 class="animated-title">¡Aprende a tocar batería con nosotros!</h1>
          <p class="animated-subtitle">
            No necesitas experiencia previa, nosotros te enseñamos desde cero. Descubre el ritmo y la magia de la batería.
          </p>
          <button class="cta-button">¡Comienza hoy!</button>
        </div>
        <div class="hero-image"></div>
      </section>
  
      <!-- About Section -->
      <section id="about">
        <h2>¿Por qué aprender batería?</h2>
        <div class="about-content">
          <p>
            La batería es el corazón de la música. Aprender a tocarla mejora tu coordinación, creatividad y concentración. ¡Es un reto divertido y una excelente forma de relajarte mientras disfrutas de la música!
          </p>
          <p>
            Además, aprender a tocar la batería te abre a una nueva forma de expresión artística, mejora tu agilidad mental y te conecta con una comunidad global de músicos.
          </p>
        </div>
      </section>
  
      <!-- No Need Experience Section -->
      <section id="no-experience">
        <h2>No necesitas experiencia previa</h2>
        <p>
          Si nunca has tocado batería antes, ¡no te preocupes! Con nosotros aprenderás todo lo que necesitas saber, desde los conceptos básicos hasta técnicas avanzadas.
        </p>
        <p>
          Nuestros cursos están diseñados para adaptarse a tu ritmo, así que podrás avanzar a tu propio ritmo y disfrutar cada paso del camino.
        </p>
      </section>
  
      <!-- Teachers Section -->
      <section id="teachers">
        <h2>Conoce a Nuestros Profesores</h2>
        <div class="cards">
          <div class="card" v-for="teacher in teachers" :key="teacher.id">
            <img :src="teacher.image" :alt="teacher.name" />
            <h3>{{ teacher.name }}</h3>
            <p>{{ teacher.bio }}</p>
            <div class="teacher-details">
              <p>Tipo de clase: {{ teacher.type }}</p>
              <p>Precio: {{ teacher.price }}</p>
              <p class="rating">
                <span v-for="n in 5" :key="n" :class="n <= teacher.rating ? 'star filled' : 'star'">★</span>
                ({{ teacher.rating }})
              </p>
            </div>
            <button class="contact-button">Contáctanos</button>
          </div>
        </div>
      </section>
  
      <!-- Join Section -->
      <section id="join">
        <h2>¡Es tu momento de empezar a tocar!</h2>
        <p>No importa tu nivel de habilidad. Aquí aprenderás a tocar a tu ritmo, ¡y pronto estarás tocando como un experto!</p>
        <button class="cta-button">¡Reserva tu lugar ahora!</button>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Aprende',
    data() {
      return {
        teachers: [
          {
            id: 1,
            name: 'Juan Pérez',
            bio: 'Percusionista con más de 10 años de experiencia, apasionado por enseñar de forma divertida.',
            price: '$15 por clase',
            type: 'Presencial',
            rating: 4,
            image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1gJOwkbAOlH4u4P7owj_h3wBpIL-7MIsiqg&s',
          },
          {
            id: 2,
            name: 'Ana López',
            bio: 'Especialista en técnicas avanzadas y percusión moderna. Gran habilidad para clases virtuales.',
            price: '$18 por clase',
            type: 'Virtual',
            rating: 5,
            image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJFunnvAHlbcoSGDtehTX78vDdyfKCMS9K8RBALOSpEEUwLuass9fOVIB6wydWp9VbP1A&usqp=CAU',
          },
          {
            id: 3,
            name: 'Carlos Díaz',
            bio: 'Músico profesional y docente con enfoque en ritmos latinos y baterías electrónicas.',
            price: '$20 por clase',
            type: 'Presencial',
            rating: 4.5,
            image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmBpyu2u6MvHBxaOUqOYdwGDvnFJezWUzlyA&s',
          },
          {
            id: 4,
            name: 'Marta Gómez',
            bio: 'Baterista con experiencia en jazz y música experimental. Clases llenas de energía y creatividad.',
            price: '$22 por clase',
            type: 'Virtual',
            rating: 4.8,
            image: 'https://img.freepik.com/fotos-premium/baterista-caucasiano-improvisando-isolado-no-fundo-azul-do-estudio-sob-luz-de-neon_489646-21482.jpg?semt=ais_hybrid',
          },
          {
            id: 5,
            name: 'Pedro Silva',
            bio: 'Músico de banda con enfoque en técnicas de percusión para principiantes.',
            price: '$17 por clase',
            type: 'Presencial',
            rating: 4.2,
            image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXFWT7R4tJVP6I2GzGcuK16BVoyRC4-x0rlg&s',
          },
          {
            id: 6,
            name: 'Isabel Rodríguez',
            bio: 'Baterista experimental y docente de técnicas alternativas de percusión.',
            price: '$19 por clase',
            type: 'Virtual',
            rating: 5,
            image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdtdd5IQVNDj5RrEZbcraemh-m6um7UFBGKXWEm9z6CUORzSCO6saMqyq9XtNpjb0I5x4&usqp=CAU',
          },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  /* General Styles */
  #aprende-page {
    font-family: 'Arial', sans-serif;
    color: #333;
    background: url('https://images.unsplash.com/photo-1524230659092-07f99a75c013?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8dG9jYW5kbyUyMGJhdGVyaWF8ZW58MHx8MHx8fDA%3D') no-repeat center center fixed;
    background-size: cover;
  }
  
  /* Hero Section */
  #hero {
    display: flex;
    justify-content: space-between;
    padding: 50px;
    background-color: rgba(0, 0, 0, 0.6);
    color: white;
    position: relative;
    border-bottom: 2px solid #fff;
  }
  
  .hero-content {
    max-width: 50%;
    z-index: 2;
  }
  
  .animated-title {
    font-size: 3.5rem;
    animation: fadeIn 2s ease-out;
    font-weight: bold;
  }
  
  .animated-subtitle {
    font-size: 1.5rem;
    margin: 15px 0;
    animation: slideUp 2s ease-out;
  }
  
  .cta-button {
    background-color: #ff9800;
    padding: 15px 30px;
    border-radius: 8px;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.3s ease;
    margin-top: 20px;
  }
  
  .cta-button:hover {
    background-color: #f57c00;
    transform: scale(1.1);
  }
  
  /* About Section */
  #about {
    padding: 50px;
    background-color: rgba(255, 255, 255, 0.9);
    text-align: center;
    border-top: 2px solid #2c3e50;
  }
  
  #about h2 {
    font-size: 2.5rem;
    margin-bottom: 20px;
    color: #2c3e50;
  }
  
  #about p {
    font-size: 1.2rem;
    color: #7f8c8d;
  }
  
  /* No Experience Section */
  #no-experience {
    padding: 50px;
    background-color: rgba(46, 204, 113, 0.2);
    text-align: center;
    border-top: 2px solid #27ae60;
  }
  
  #no-experience h2 {
    font-size: 2.5rem;
    margin-bottom: 20px;
  }
  
  #no-experience p {
    font-size: 1.2rem;
    color: #7f8c8d;
  }
  
  /* Teachers Section */
  #teachers {
    padding: 50px;
    background-color: #f7f7f7;
  }
  
  #teachers h2 {
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 30px;
    color: #2c3e50;
  }
  
  .cards {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 20px;
  }
  
  .card {
    background-color: white;
    width: 30%;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .card:hover {
    transform: translateY(-10px);
    box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
  }
  
  .card img {
    width: 100%;
    height: auto;
    border-radius: 8px;
  }
  
  .card h3 {
    font-size: 1.8rem;
    margin: 10px 0;
  }
  
  .card p {
    font-size: 1.1rem;
    color: #7f8c8d;
  }
  
  .teacher-details {
    margin-top: 10px;
  }
  
  .teacher-details p {
    font-size: 1.1rem;
  }
  
  .rating {
    color: #f39c12;
  }
  
  .rating .star {
    color: #bdc3c7;
  }
  
  .rating .star.filled {
    color: #f39c12;
  }
  
  .contact-button {
    background-color: #2ecc71;
    padding: 10px 20px;
    border-radius: 8px;
    color: white;
    font-size: 1.1rem;
    cursor: pointer;
    margin-top: 15px;
    transition: background-color 0.3s ease, transform 0.3s ease;
  }
  
  .contact-button:hover {
    background-color: #27ae60;
    transform: scale(1.05);
  }
  
  /* Join Section */
  #join {
    padding: 50px;
    background-color: #ecf0f1;
    text-align: center;
  }
  
  #join h2 {
    font-size: 2.5rem;
    margin-bottom: 20px;
  }
  
  #join p {
    font-size: 1.2rem;
    color: #7f8c8d;
  }
  
  </style>
  