<template>
    <div class="place-card">
        <div class="place-image">
            <img src="https://a0.muscache.com/4ea/air/v2/pictures/505d7045-4372-4713-9b11-efc8a9914822.jpg?t=r:w2500-h1500-sfit,e:fjpg-c90" alt="">
        </div>

        <div class="place-meta">
            <h2 class="section-title">Sydney from Our Huge, Stylish Apartment</h2>
            <div class="place-type">Private Room</div>
            <div class="rating-review d-flex">$25/night</div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "PlaceCard"
    }
</script>

<style scoped>
    .place-card{
        border: 1px solid #dadada;
        padding: 10px;

    }
    .place-image {
        margin: 0 0 5px 0;
    }

    .place-meta .section-title {
        font-size: 20px;
        line-height: 24px;
        font-weight: 600;
        margin-top: 4px;

    }
</style>