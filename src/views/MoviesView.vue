<script setup>
import {ref, onMounted } from "vue";

let movies = ref([]);

function fetchMovies(){
  fetch('/api/v1/movies')

  .then(function(response){
    return response.json();
  })

  .then(function(data) {
  console.log(data.movies)  // check what poster value looks like
  movies.value = data.movies;
  })

  .catch(function(error){
    console.error("Failed to fetch movies:", error);
  })


}

onMounted(() => {
  fetchMovies()
    
  })




</script>

<template>
  <div class="container">
    <h1>Movies</h1>
    <div class="movies-container">
      <div v-for="movie in movies" :key="movie.id" class="movie">
        <div class="img">
          <img :src="movie.poster" alt="Image">
        </div>
        <div class="content">
          <h2>{{ movie.title }}</h2>
          <p>{{ movie.description }}</p>
        </div>
      </div>


    </div>

  </div>

</template>

<style scoped>

.container{
  margin: 0, auto;
  padding: 20px;
  max-width: 1100px;
}

h1{
  text-align: left;
  margin-bottom: 30px;
  font-size: 2.5rem;
}

.movies-container{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 25px;
}

.movie{
  display: flex;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 6px 15px rgba(0, 114, 180, 0.2);
  transition: transform 0.3s ease box-shadow 0.3s ease;
  max-height: 300px;
  border: 0.5px solid grey;
}

.movie:hover{
   box-shadow: 0 6px 15px rgba(0, 114, 180, 0.6);
   transform: translateY(-8px);
   cursor: pointer;
}

.img{
  width: 40%;
  height: 100%;
}

.img img{
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.content{
  display: flex;
  flex-direction: column;
  width: 60%;
  padding: 15px;
}

.content h2{
  font-size: 1.7rem;
  margin-bottom: 10px;
}

.content p{
  color: #555;
  line-height: 1.5;
}



</style>