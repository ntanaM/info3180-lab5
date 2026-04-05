<script setup>
  import {ref, onMounted} from "vue";

  onMounted(() => {
    getCsrfToken();
  })

  let csrf_token = ref("");

  function getCsrfToken() {
    return fetch('/api/v1/csrf-token')
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        csrf_token.value = data.csrf_token
      })
      .catch((error) => {
        console.log(error)
      })
}


  
   function saveMovie() {

    let movieForm = document.getElementById('movieForm')
    let form_data = new FormData(movieForm)

    fetch("/api/v1/movies", {
      method: 'POST',
      body: form_data,
      credentials: 'include', 
      headers: {
        'X-CSRFToken': csrf_token.value,
      }
    })

    .then(function(response){
      return response.json();
    })

    .then(function (data){
      console.log(data)
    })

    .catch(function (error){
      console.log(error)
    })

  }

</script>

<template>
  <div class="form-container">
    <h2>Upload Form</h2>

    <form @submit.prevent="saveMovie" enctype="multipart/form-data" id="movieForm">
      <div class="item">
        <label for="title">Title</label>
        <input type="text" name="title" id="title">
      </div>

      <div class="item">
        <label for="description">Descripton</label>
        <textarea name="description" id="description"></textarea>
      </div>

      <div class="item">
        <label for="poster">Photo Upload</label>
        <input type="file" name="poster" id="poster" />
      </div>

      <button type="submit">Submit</button>
    </form>

    <!-- Flash Error Message -->


  </div>

</template>

<style>
.form-container{
  max-width: 400px;
  margin: auto;
}

form{
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: center;
  gap: 20px;
}

.item{
  display: flex;
  flex-direction: column;
  gap: 10px;

}

button{
  border: none;
  border-radius: 10px;
  padding: 10px;
  width: 90px;
  background-color: rgb(27, 125, 223);
  color: white;
  font-weight: 1000px;
}

button:hover{
  background-color: rgb(63, 179, 225);
}


</style>