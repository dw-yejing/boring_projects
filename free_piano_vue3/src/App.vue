<template>
  <router-view></router-view>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
::-webkit-scrollbar {
  width: 0px;
  height: 0px;
  background-color: #F5F5F5;
  display: none;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

html, body {
  width: 100%;
  height: 100%;
  user-select: none;
  position: relative;
  overflow-x: scroll;
  overflow-y: hidden;
}

#app {
  width: 100%;
  height: 100%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
