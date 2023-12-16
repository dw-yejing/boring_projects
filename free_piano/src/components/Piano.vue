<style scoped lang="less">
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
.switchWP{
    -webkit-animation: swing 2000ms infinite alternate ease-in-out;
    animation: swing 2000ms infinite alternate ease-in-out;
    @keyframes swing {
        0% {top: -50px}
        50% {top: -70px;}
        100% {top: -50px;}
    }

    @keyframes swing {
        0% {top: -50px}
        50% {top: -70px;}
        100% {top: -50px;}
    }
    position: absolute;
    left: 3%;
    top: -50px;
    #string{
        width: .1rem;
        border-right: .1rem solid #777;
        height: 45vmin;
    }
    #box{
        &:hover { cursor: pointer; }
        margin: 0 15px;
        display: inline-block;
        height: 50px;
        line-height: 50px;
        width: 50px;
        background-image: url('/static/images/camera.png');
        background-repeat:no-repeat;
        background-size:100% 100%;
        -moz-background-size:100% 100%;
        margin-top: -20px;
        margin-left: -15px;
    }
}
.piano-band{
    width: 100%;
    height: 40px;
    line-height: 40px;
    background: #000;
    box-shadow: inset 0 -1px 2px hsla(0,0%,100%,.4), 0 2px 3px rgba(0,0,0,.4);
    border-width: 3px 2px 2px;
    border-style: solid;
    border-color: #555 #222 #111 #777;
    position: relative;
    .piano-band-img{
        width: 130px;
        height: 100%;
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
    }
    .piano-tip{
        position: absolute;
        top: 50%;
        right: 20px;
        transform: translateY(-50%);
        color: #fff;
        font-size: 14px;
    }
}
.piano-wrap{
    width: 90%;
    margin: 0 auto;
    box-shadow: 2px 2px 10px 2px #aaa;
    border-radius: 5px;
    position: relative;
    overflow: hidden;
    background: #373737;
    .wkeyWrap{
        &:hover{cursor: pointer;}
        height: 223.65px;
        overflow: hidden;
        position: relative;
        width: 100%;
        .wkey{
            display: inline-block;
            width: 2.775%;
            height: 100%;
            margin: 0 auto;
            background: linear-gradient(-30deg,#f5f5f5,#fff);
            box-shadow: inset 0 1px 0 #fff, inset 0 -1px 0 #fff, inset 1px 0 0 #fff, inset -1px 0 0 #fff, 0 4px 3px rgba(0,0,0,.7);
            border-radius: 0 0 5px 5px;
            position: relative;
            &:active { box-shadow:0 2px 2px rgba(0,0,0,0.4); top: -1%; height: 99%;  background:#efefef; }
            &:active:before { content:""; border-width:250px 5px 0px; border-style:solid; border-color:transparent transparent transparent rgba(0,0,0,0.1); position: absolute; left: 0; bottom: 0; }
            &:active:after { content:""; border-width:250px 5px 0px; border-style:solid; border-color:transparent rgba(0,0,0,0.1) transparent transparent; position: absolute; right: 0; bottom: 0; }
            .keytip{
                text-align: center;
                width: 100%;
                color: #373737;
                position: absolute;
                left: 0;
                bottom: 5%;
                font-size: 14px;
                overflow: hidden;
                .keyname{
                    margin-bottom: 5px;
                    font-weight: 700;
                }
                .notename, .singname{
                    display: inline-block;
                    width: 20px;
                    height: 20px;
                    line-height: 20px;
                    text-align: center;
                    font-weight: 700;
                }
            }
        }
        .wkey-active { box-shadow:0 2px 2px rgba(0,0,0,0.4); top: -1%; height: 99%; background: #efefef;
            &:before { content:""; border-width:250px 5px 0px; border-style:solid; border-color:transparent transparent transparent rgba(0,0,0,0.1); position: absolute; left: 0; bottom: 0; }
            &:after { content:""; border-width:250px 5px 0px; border-style:solid; border-color:transparent rgba(0,0,0,0.1) transparent transparent; position: absolute; right: 0; bottom: 0; }
        }
    }

    .bkeyWrap{
        &:hover{cursor:pointer;}
        width: 20%;
        height: 145.373px;
        display: inline-block;
        .bkey{
            display: inline-block;
            width: 10%;
            height: 145.373px;
            background: linear-gradient(-20deg,#333,#000,#333);
            border-width: 1px 2px 7px;
            border-style: solid;
            border-color: #666 #222 #111 #555;
            border-radius: 0 0 2px 2px;
            box-shadow: inset 0 -1px 2px hsla(0,0%,100%,.4), 0 2px 3px rgba(0,0,0,.4);
            position: absolute;
            top: 44px;
            overflow: hidden;
            &:active { height:101%; border-bottom-width:2px; box-shadow:inset 0px -1px 1px rgba(255,255,255,0.4),0 1px 0px rgba(0,0,0,0.8),0 2px 2px rgba(0,0,0,0.4),0 -1px 0px #000; }
            .keytip{
                width: 100%;
                color: #fff;
                position: absolute;
                text-align: center;
                bottom: 5%;
                font-size: 14px;
                overflow: hidden;
            }
        }
        .bkey-active { height:101%; border-bottom-width:2px; box-shadow:inset 0px -1px 1px rgba(255,255,255,0.4),0 1px 0px rgba(0,0,0,0.8),0 2px 2px rgba(0,0,0,0.4),0 -1px 0px #000; }
    }
    .wkey:nth-child(36){ .notename,.singname{background-color: #ee8055;} }
    .wkey:nth-child(-n+35){ .notename,.singname{background-color: #ee8055;} }
    .wkey:nth-child(-n+28){ .notename,.singname{background-color: #fbb957;} }
    .wkey:nth-child(-n+21){ .notename,.singname{background-color: #a4cab6;} }
    .wkey:nth-child(-n+14){ .notename,.singname{background-color: #93b5cf;} }
    .wkey:nth-child(-n+7){ .notename,.singname{background-color: #ccccd6;} }

    .bkey:nth-child(1) { left: 9%; }
    .bkey:nth-child(2) { left: 23%; }
    .bkey:nth-child(3) { left: 50%; }
    .bkey:nth-child(4) { left: 65%; }
    .bkey:nth-child(5) { left: 79%; }

    .bkeyWrap { width: 20%; position: absolute; top: 0; }
    .bkeyWrap:nth-child(2) { left: 0; }
    .bkeyWrap:nth-child(3) { left: 19.5%; }
    .bkeyWrap:nth-child(4) { left: 39%; }
    .bkeyWrap:nth-child(5) { left: 58.3%; }
    .bkeyWrap:nth-child(6) { left: 77.7%; }
}

.piano-options{
    height: 50px;
    margin: 10px auto 15px;
    padding: 0;
    position: relative;
    width: 85%;
    .option-item-wrap{
        position: absolute;
        right: 1%;
        .option-item{
            display: inline-block;
            height: 50px;
            line-height: 50px;
            margin: 0 15px;
            .label{
                // Hide the ugly checkbox
                > input { display: none; }
                // New beautiful checkbox
                i { display: inline-block; margin-left: 5px; padding: 2px; width: 40px; height: 20px; border-radius: 13px; vertical-align: middle; transition: .25s .09s; position: relative; background: #d8d9db; box-sizing: initial;
                &:after { content: " "; display: block; width: 20px; height: 20px; border-radius: 50%; background: #fff; position: absolute; left: 2px; transition: .25s; }
                }
                // Checked-state
                > input:checked + i { background: #07E26D; }
                > input:checked + i:after { transform: translateX(20px); }
                // Label-hover
                &:hover { cursor: pointer; }
            }
        }    
    }   
}

</style>

<template>
    <div class="piano">
        <div class="switchWP">
            <div id="string"></div>
            <div id="box" @click.stop="emitChangeWallPaper"></div>
        </div>
        <div class="piano-wrap">
            <div class="piano-band">
            <img class="piano-band-img" src="@/assets/images/band.png" alt="">
            <div class="piano-tip">⇧ 代表 space 键</div>
            </div>
            <div class="piano-key-wrap">
                <div class="wkeyWrap">
                    <div class="wkey" v-for="note in wNotes" :key="note.id" @click.stop="clickPianoKey($event, note.keyCode)" :data-keyCode="note.keyCode">
                        <div class="keytip">
                            <div class="keyname" v-show="showKeyName">{{note.key}}</div>
                            <div class="notename" v-show="showNoteName">{{note.name}}</div>
                        </div>
                    </div>
                </div>
                <div class="bkeyWrap" >
                    <div class="bkey" v-for="note in bNotes_1" :key="note.id"  @click.stop="clickPianoKey($event, note.keyCode)" :data-keyCode="note.keyCode">
                        <div class="keytip">
                            <div class="keyname" v-html="note.key" v-show="showKeyName"></div>
                        </div>
                    </div>
                </div>
                <div class="bkeyWrap" >
                    <div class="bkey" v-for="note in bNotes_2" :key="note.id"  @click.stop="clickPianoKey($event, note.keyCode)" :data-keyCode="note.keyCode">
                        <div class="keytip">
                            <div class="keyname" v-html="note.key" v-show="showKeyName"></div>
                        </div>
                    </div>
                </div>
                <div class="bkeyWrap" >
                    <div class="bkey" v-for="note in bNotes_3" :key="note.id"  @click.stop="clickPianoKey($event, note.keyCode)" :data-keyCode="note.keyCode">
                        <div class="keytip">
                            <div class="keyname" v-html="note.key" v-show="showKeyName"></div>
                        </div>
                    </div>
                </div>
                <div class="bkeyWrap" >
                    <div class="bkey" v-for="note in bNotes_4" :key="note.id" @click.stop="clickPianoKey($event, note.keyCode)" :data-keyCode="note.keyCode">
                        <div class="keytip">
                            <div class="keyname" v-html="note.key" v-show="showKeyName"></div>
                        </div>
                    </div>
                </div>
                <div class="bkeyWrap" >
                    <div class="bkey" v-for="note in bNotes_5" :key="note.id" @click.stop="clickPianoKey($event, note.keyCode)" :data-keyCode="note.keyCode">
                        <div class="keytip">
                            <div class="keyname" v-html="note.key" v-show="showKeyName"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="piano-options responsive-section-a">
                
                <div class="option-item-wrap">
                    <div class="option-item">
                    <label class="label">
                        显示按键提示
                        <input type="checkbox" id="keyname" v-model="showKeyName" />
                        <i></i>
                    </label>
                    </div>

                    <div class="option-item">
                    <label class="label">
                        显示音名
                        <input type="checkbox" id="notename" v-model="showNoteName" />
                        <i></i>
                    </label>
                    </div>
                </div>
            </div>
    </div>
</template>

<script>
import Tone from 'tone'
import Notes from "@/assets/js/notes";
import SmapleLibrary from '@/lib/Tonejs-Instruments'
import WallPaper from "@/assets/js/wallpaper";

export default {
    name: 'Piano',
    data: function(){
        return{
            Notes: Notes,
            showKeyName: true,
            showNoteName: true,
            wallpaperLoading: false,
        }
    },
    components: {},
    mounted: function(){
        this.initPiano();
    },
    methods: {
        // 钢琴初始化
        async initPiano() {
            setTimeout(() => {
                //this.computeEleSize()
                this.pianoShow = true
            }, 300)
            this.bindKeyBoradEvent()

            this.synth = SmapleLibrary.load({
                instruments: "piano"
            }).toMaster();
        },
        // 鼠标操作，点击按键播放
        clickPianoKey(e, keyCode) {
            let pressedNote = this.getNoteByKeyCode(keyCode)
            if (pressedNote) {
                this.playNote(pressedNote.name)
            }
        },
        computeEleSize() {
            let wkey_width = $('.piano-key-wrap').width() / 36;
            let wkey_height = wkey_width * 7;
            let bkey_height = wkey_height * 0.7;
            $('.piano-key-wrap').height(wkey_height);
            $('.bkey').height(bkey_height);
        },

        // 键盘操作 核心代码
        bindKeyBoradEvent() {
            const ShiftKeyCode = 16;
            const SpaceKeyCode = 32;
            document.addEventListener('keydown', (e) => {
                let keyCode = e.keyCode;
                if (this.DEV) console.log('keydown', keyCode);
                // 按住Shfit键，则启用黑色按键
                // if (keyCode == ShiftKeyCode) {
                if (keyCode == SpaceKeyCode) {
                e.preventDefault();
                this.enableBlackKey = true
                }
                if (this.enableBlackKey) keyCode = 'b' + keyCode

                if (keyCode == this.lastKeyCode) {
                // 连续触发同一个键时，应节流 + 延音
                if (!this.keyLock) {
                    this.playNoteByKeyCode(keyCode)
                    // 这里应该延音，解决中...
                    this.lastKeyCode = keyCode
                    this.keyLock = true
                }
                if (this.keydownTimer) {
                    clearTimeout(this.keydownTimer)
                    this.keydownTimer = null
                }
                this.keydownTimer = setTimeout(() => {
                    this.keyLock = false
                }, 120)
                } else {
                this.playNoteByKeyCode(keyCode)
                this.lastKeyCode = keyCode
                }
            }, false);

            document.addEventListener('keyup', (e) => {
                // console.log('keyup');
                let keyCode = e.keyCode;
                // 松开Shfit键，则禁用黑色按键
                // if (keyCode == ShiftKeyCode) {
                if (keyCode == SpaceKeyCode) {
                    e.preventDefault();
                    this.enableBlackKey = false;
                }
                $(`.wkey`).removeClass('wkey-active')
                $(`.bkey`).removeClass('bkey-active')
            }, false)
        },
        getNoteByKeyCode(keyCode) {
            // 改为更高性能的写法
            let target
            let len = this.Notes.length || 0
            for (let i = 0; i < len; i++) {
                let note = this.Notes[i]
                if (note.keyCode == keyCode) {
                    target = note
                    break
                }
            }
            return target
        },
        // 根据键值播放音符
        playNoteByKeyCode(keyCode) {
            let pressedNote = this.getNoteByKeyCode(keyCode)
            if (pressedNote) {
                this.playNote(pressedNote.name)
                let keyType = pressedNote.type;
                if (keyType == 'white') {
                    $(`[data-keyCode=${pressedNote.keyCode}]`).addClass('wkey-active');
                } else if (keyType == 'black') {
                    $(`[data-keyCode=${pressedNote.keyCode}]`).addClass('bkey-active');
                }
            }
        },
        // 触发单个音符播放
        playNote(notename = 'C4', duration = '1n') {
            if (!this.synth) return
            try {
                this.synth.triggerAttackRelease(notename, duration);
            } catch (e) {}
        },
        // 随机背景壁纸
        emitChangeWallPaper() {
            if(this.wallpaperLoading){
                //等待加载
                return;
            }
            this.wallpaperLoading = true
            let len = WallPaper.length
            let src = ''
            do {
                let random = Math.floor(Math.random() * len)
                src = WallPaper[random]
            } while (!src || src == this.$parent.currentWallpaper)

            let img = new Image();
            img.src = src
            img.onload = () => {
                this.wallpaperLoading = false;
                this.$parent.currentWallpaper=src;
                img = null
            }
        },
       
    },
    computed: {
        wNotes: function(){
            return this.Notes.filter(function(note){
                return note.type=='white';
            })
        },
        bNotes_1: function(){
            return this.Notes.filter(function(note){
                return note.type=='black' && note.id >= 36 && note.id <= 40;
            })
        },
        bNotes_2: function(){
            return this.Notes.filter(function(note){
                return note.type=='black' && note.id >= 41 && note.id <= 45;
            })
        },
        bNotes_3: function(){
            return this.Notes.filter(function(note){
                return note.type=='black' && note.id >= 46 && note.id <= 50;
            })
        },
        bNotes_4: function(){
            return this.Notes.filter(function(note){
                return note.type=='black' && note.id >= 51 && note.id <= 55;
            })
        },
        bNotes_5: function(){
            return this.Notes.filter(function(note){
                return note.type=='black' && note.id >= 56 && note.id <= 60;
            })
        },
        
    }

}
</script>