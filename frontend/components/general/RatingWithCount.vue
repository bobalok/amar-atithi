<template>
    <div class="RatingWithCount d-flex">
        <StarRating class="StarRating"/>
        <span class="count">93</span>
    </div>
</template>

<script>
    import StarRating from "./StarRating";
    export default {
        name: "RatingWithCount",
        components: {StarRating}
    }
</script>

<style scoped>
.count{
    margin-left: 4px;
}

    .StarRating{
        margin-top: 2px;
    }


</style>