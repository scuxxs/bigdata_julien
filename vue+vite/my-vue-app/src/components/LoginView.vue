<template>
  <div class="body">
    <div class="main">
      <div class="switch" id="switch-cnt">
        <div class="switch__circle"></div>
        <div class="switch__circle switch__circle--t"></div>
        <div class="switch__container" id="switch-c1">
          <h2 class="switch__title title">Welcome Back !</h2>
          <p class="switch__description description">To keep connected with us please login with your personal info</p>
          <button class="switch__button button switch-btn" @click="change">SIGN IN</button>
        </div>
        <div class="switch__container is-hidden" id="switch-c2">
          <h2 class="switch__title title">Hello Friend !</h2>
          <p class="switch__description description">Enter your personal details and start journey with us</p>
          <button class="switch__button button switch-btn" @click="change">SIGN UP</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const change = () => {
  const switchC1 = document.querySelector("#switch-c1") as any;
  const switchC2 = document.querySelector("#switch-c2") as any;
  const switchCircle = document.querySelectorAll(".switch__circle") as any;
  const switchCtn = document.querySelector("#switch-cnt") as any;
  switchCtn.classList.add("is-gx");
  setTimeout(function(){
    switchCtn.classList.remove("is-gx");
  }, 1500)
  switchCtn.classList.toggle("is-txr");
  switchCircle[0].classList.toggle("is-txr");
  switchCircle[1].classList.toggle("is-txr");
  switchC1.classList.toggle("is-hidden");
  switchC2.classList.toggle("is-hidden");
}
</script>


<style scoped >
*, *::after, *::before {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  user-select: none;
}

.body {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "Montserrat", sans-serif;
  font-size: 12px;
  background-color: #ecf0f3;
  color: #a0a5a8;
}

.main {
  position: relative;
  width: 1000px;
  min-width: 1000px;
  min-height: 600px;
  height: 600px;
  padding: 25px;
  background-color: #ecf0f3;
  box-shadow: 10px 10px 10px #d1d9e6, -10px -10px 10px #f9f9f9;
  border-radius: 20px;
  overflow: hidden;
}
@media (max-width: 1200px) {
  .main {
    transform: scale(0.7);
  }
}
@media (max-width: 1000px) {
  .main {
    transform: scale(0.6);
  }
}
@media (max-width: 800px) {
  .main {
    transform: scale(0.5);
  }
}
@media (max-width: 600px) {
  .main {
    transform: scale(0.4);
  }
}
.is-hidden{
  opacity: 0;
  position: absolute;
  transition: 1.25s;
}
.is-gx{
  animation: is-gx 1.25s;
}
@keyframes is-gx {
  0%,10%,100%{
    width: 400px;
  }
  30%,50%{
    width: 500px;
  }
}
</style>