<template>
    <div class="home">
        <div class="app-bg" :style="appBgStyle"></div>
        <div class="app-content">
            <Piano @update-wallpaper="updateWallpaper"></Piano>
            <Score></Score>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Piano from "@/components/Piano"
import Score from "@/components/Score"

const currentWallpaper = ref("/images/backgrounds/bg_1.jpg")

const appBgStyle = computed(() => {
    return `background-image: url(${currentWallpaper.value});`
})

const updateWallpaper = (src) => {
    currentWallpaper.value = src
}
</script>

<style scoped lang="less">
.home{
    width: 100%;
    height: 100%;
    overflow-x: scroll;
}
.app-bg{
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: -100;
    opacity: .5;
    background-size: cover;
    background-repeat: no-repeat;
}
.app-content{
    width: 100%;
    height: 100%;
    overflow-y: scroll;
    position: relative;
}
</style>