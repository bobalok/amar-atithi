<template>
    <div class="place-card" v-if="place">
        <div class="card-image" ref="CardImage" v-if="place.cover">
            <v-img
                    :src="place.cover.file"
                    lazy-src="https://picsum.photos/id/11/10/6"
                    aspect-ratio="1.5"
            ></v-img>
        </div>

        <div class="card-meta">
            <div class="place-type">{{place.space.name}} <span class="ml-1 mr-1"> · </span> {{place.state}}</div>
            <h2 class="place-title"><nuxt-link :to="{name: 'places-code', params: {code: place.code}}">{{place.title}}</nuxt-link></h2>
            <div class="property-price">{{$Settings.Price(place.price)}}/night</div>

            <div class="place-rating">
                <StarRating :value="place.rating"/>
                <span class="review_count">{{place.rating_count > 1 ? place.rating_count + ' Reviews' : place.rating_count + ' Review' }}</span>
            </div>
        </div>
    </div>
</template>

<script>
    import StarRating from "../general/StarRating";
    export default {
        name: "PlaceCard",
        components: {StarRating},
        props: ['place'],
        mounted() {

        }
    }
</script>

<style lang="scss" scoped>


    h2.place-title {
        font-weight: 600;
        font-size: 1.2rem;
        line-height: 1.3em;
        margin: 4px 0 4px;
        display: block;

        a{
            color: inherit;
        }
    }

    .place-type {
        font-size: .95rem;
        color: rgb(118, 118, 118);
        font-weight: 500;
    }

    .card-meta {
        color: rgb(72, 72, 72);
    }



    .place-rating {
        font-size: 13px;
        display: flex;
        margin-top: 1px;
    }

    span.review_count {
        margin-left: 5px;
    }

    .place-card {
        margin: 0 0 10px 0;
    }

    .card-image{
        margin-bottom: 4px;
    }

    .star-ratings {
        position: relative;
        font-size: 14px;
        margin-top: 2px;
    }

</style>