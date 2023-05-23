<template>
    <div class="star-ratings">
        <div class="star-list-unfilled">
            <div class="star-list star-list-empty">
                <i class="la la-star"></i>
                <i class="la la-star"></i>
                <i class="la la-star"></i>
                <i class="la la-star"></i>
                <i class="la la-star"></i>
            </div>
        </div>

        <div class="star-list-overlay">
            <div class="star-list primary--text" :style="Rating">
                <i class="la la-star "></i>
                <i class="la la-star"></i>
                <i class="la la-star"></i>
                <i class="la la-star"></i>
                <i class="la la-star"></i>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "StarRating",
        props: ['value'],
        computed:{
            Rating(){
                let val = (this.value /5.00) * 1000
                return {
                    width: `${val}%`
                }
            }
        }
    }
</script>

<style scoped>
    .star-list-overlay,
    .star-list-unfilled {
        position: relative;
        height: 15px;
        width: 78px;
    }

    .star-list-overlay {
        margin-top: -15px;
    }

    .star-list.primary--text {
        width: 91%;
        overflow: hidden;
        position: relative;
        height: 100%;
    }

    .star-list i {
        position: absolute;
        left: 0;
        width: 14px;
        height: 14px;
    }

    .star-list i:nth-child(2) {
        left: 16px;
    }

    .star-list i:nth-child(3) {
        left: 32px;
    }

    .star-list i:nth-child(4) {
        left: 48px;
    }

    .star-list i:nth-child(5) {
        left: 64px;
    }

    .star-list.star-list-filled.primary--text {
        position: absolute;
        top: 0;
        overflow: hidden;
    }

    .star-ratings {
        position: relative;
    }
</style>