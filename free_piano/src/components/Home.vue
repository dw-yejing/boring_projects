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

<template>
    <div class="home">
        <div class="app-bg" :style="appBgStyle"></div>
        <div class="app-content">
            <Piano></Piano>
            <Score></Score>
        </div>
    </div>
</template>>

<script>
import Piano from "@/components/Piano";
import Score from "@/components/Score";

export default{
    data: function() {
        return {
            ///static/images/bg_default.jpg
            currentWallpaper:'https://api.neweb.top/bing.php',
        }
    },
    components:{
        Piano,
        Score
    },
    computed:{
        appBgStyle() {
            return `background-image: url(${this.currentWallpaper});`
        },
    },
    methods: {
         
    }
}
</script>