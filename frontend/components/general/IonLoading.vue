<template>
    <div class="LoadingBlock text-xs-center">
        <div class="LoadingInner" :style="LoadingInnerStyle">
            <img :style="LoaderStyle" src="../../assets/media/moving-block.gif"/>
            <div class="block_text">{{LoadingText}}</div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "IonLoading",
        props: ['size', 'text'],
        computed: {
            ImageSize() {
                return this.size || 65;
            },
            LoadingText() {
                return this.text || "Loading the data. Please wait....."
            },
            LoaderStyle() {
                return {
                    'height': this.ImageSize + "px"
                }
            },
            LoadingInnerStyle() {
                return {
                    'margin-top': ((this.ImageSize / 2) * -1) - 10 + "px"
                }
            }
        }
    }
</script>

<style lang="scss" scoped>

    .LoadingBlock {

        width: 100%;

        background: transparent;
        display: block;
        vertical-align: middle;

        .LoadingInner {
            position: absolute;
            top: 50%;
            margin-left: -150px;
            margin-top: -60px;
            width: 300px;
            text-align: center;
            display: block;
            left: 50%;

            img {
                height: 90px;
            }

            span {
                display: block;
            }
        }
    }
</style>
