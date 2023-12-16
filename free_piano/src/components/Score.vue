<style lang="less" scoped>
.score{
    display: flex;
    width: 90%;
    margin: 0 auto;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    padding-bottom: 5%;
}
.score-list{
    width: 40%;
    min-width: 500px;
    height: 500px;
    font-size: 14px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 5px;
    border: solid 1px #ddd;
    position: relative;
    .list-view{
        width: 100%;
        height: 100%;
        position: absolute;
        top: 0;
        left: 0;
        padding: 20px 15px;
        overflow-y: scroll;
        .component-title{
            margin: 0 0 10px 0;
            font-size: 18px;
            font-weight: bold;
            position: relative;
            .degree{
                width: 150px;
                float: right;
                text-align: left;
            }
        }
        .list{
            width: 100%;
            padding-left: 25px;
            padding-bottom: 10px;
            line-height: 32px;
            .score-item{
                height: 32px;
                line-height: 32px;
                list-style: none;
                .num{
                    float: left;
                    width: 35px;
                    height: 32px;
                    font-size: 16px;
                    margin-left: -35px;
                    text-align: center;
                    color: #EF496F;
                }
                >a{
                    display: inline-block;
                    min-width: 120px;
                    cursor: pointer;
                    text-decoration: none;
                    color: #373737;
                    &:hover{
                        color: #1295DB;
                        text-decoration: underline;
                    }
                }
                .difficulty-degree{
                    width: 150px;
                    float: right;
                    text-align: left;
                    .icon-star{
                        display: inline-block;
                        width: 32px;
                        height: 32px;
                        background-position: -128px 0px;
                        vertical-align: top;
                        transform: scale(0.7);
                        margin-left: -6px;
                    }
                }
            }
            .active-item{
                background-color: #c5e0f1;
            }
        }
    }
}
.score-content{
    width: 40%;
    min-width: 500px;
    height: 500px;
    font-size: 14px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 5px;
    border: solid 1px #ddd;
    position: relative;
    overflow-y: scroll;
    .info{
        font-size: 14px;
        margin: 5px 0;
        height: 28px;
        line-height: 28px;
        text-align: center;
        background: #1295DB;
        color: #fff;
        border-radius: 2px;
    }
    .score-item-content{
        word-wrap: break-word;
        font-size: 16px;
        letter-spacing: 0;
        line-height: 26px;
        margin-left: 20px;
    }
    .score-item-lyrics{
        word-wrap: break-word;
        font-style: italic;
        margin-top: 20px;
        line-height: 26px;
        margin-left: 20px;
    }
}
</style>

<template>
    <div class="score">
        <div class="score-list">
            <div class="list-view">
                <p class="component-title">
                    <span class="title">{{ sectionTitle }}</span>
                    <span class="degree">困难度</span>
                </p>

                <ol class="list">
                    <li class="list-item score-item" v-for="(item, index) in manualscoreList" :key="index">
                    <span class="num">{{ index + 1 }}</span>
                    <a href="javascript:;" :data-no="index" @click="clickScoreItem(item, index)">{{ item.name }}</a>
                    <span class="difficulty-degree">
                         <!-- :style="starBgImage" -->
                        <i class="icon-star" :style="starBgImage" v-for="(star, sindex) in new Array(item.degree)" :key="sindex"></i>
                    </span>
                    </li>
                </ol>
            </div>
        </div>
        <div class="score-content">
            <p class="info">在键盘上依次按以下键进行演奏，注意控制节奏。</p>
            <div class="score-item-content" v-html="showItem.content || ''"></div>
            <div class="score-item-lyrics" v-html="showItem.lyrics || ''"></div>
        </div>
    </div>
   
</template>>

<script>
import ManualScore from "@/assets/js/manualscore.js"

export default {
    name:'Score',
    data: function() {
        return{
            sectionTitle: "快速入门",
            manualscoreList: ManualScore,
            showItem: {},
            starBgImage: "background-image: url('/static/images/sprite.png');",
        }
    },
    mounted: function(){
        this.clickScoreItem(this.manualscoreList[0], '0');
    },
    methods: {
        clickScoreItem(item, index) {
            if (!item || index<0) return;
            this.showItem = item;
            this.showItem.content = item.content.toUpperCase();
            $(".list li").removeClass("active-item");
            $(`[data-no=${index}]`).parent("li").addClass("active-item");
        },
    }
    
}
</script>>