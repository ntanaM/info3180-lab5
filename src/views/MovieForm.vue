<script setup>
  import {ref, onMounted} from "vue";

  onMounted(() => {
    getCsrfToken();
  })



  let csrf_token = ref("");
  let successMessage = ref("");
  let errorMessages = ref([])

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

    successMessage.value = "";
    errorMessages.value = [];

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
      console.log("Status:", response.status);
      return response.json();
    })

    .then(function (data){
      console.log(data)
      if(data.errors){
        errorMessages.value = data.errors;
      }

      else{
        successMessage.value = "File Upload Successful!"
        movieForm.reset();

        // Clear file input
        let fileInput = movieForm.querySelector('input[type="file"]')
        if (fileInput) {
          fileInput.value = ""
        }
    }
    })



      
    .catch(function (error){
      errorMessages.value = [error.message];
    })
}


</script>

<template>

  <div class="container">
    <!-- Flash Success Message -->
    <div v-if="successMessage" class="alert-success">
      {{ successMessage }}
    </div>


    <!-- Flash Error Message -->

    <div v-if="errorMessages.length" class="alert-failure">
      <ul>
        <li v-for="(error, index) in errorMessages" :key="index">
          {{ error }}
        </li>
            
      </ul>
    </div>

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

      


    </div>
  </div>

  

</template>

<style>

.container{
  display: flex;
  flex-direction: column;
  max-width: 900px;
  gap: 50px;
  margin: auto;
  padding: 20px;
}

.form-container{
  max-width: 500px;
  margin: auto;
  padding: 30px;
}

h2{
  text-align: left;
  margin-bottom: 20px;
}

form{
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.item{
  display: flex;
  flex-direction: column;
  gap: 8px;

}

label{
  font-size: 18px;
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
 background: linear-gradient(135deg, #3fb3e1, #6cc8ff);
 transform: translateY(-2px);
 cursor: pointer;

}

.alert-success{
  background: rgb(240, 253, 244);
  color: rgb(22, 101, 52);
  border: 0.5px solid rgb(134, 239, 172);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px
}

.alert-failure{
  background: rgb(254, 242, 242);
  color: rgb(153, 27, 27);
  border: 0.5px solid rgb(252, 165, 165);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px;
}

.alert-failure ul {
  margin: 0;
  padding-left: 18px;
}

.alert-failure li {
  margin: 2px 0;
}

</style>