<template>
   <v-container class="mt-8 mb-8">

       <h2 class="section-title mb-3">Your Places</h2>

       <BookingItem :place="place" :key="place.code" v-for="place in places"/>

   </v-container>
</template>

<script>
    import PlaceCard from "../../components/hosting/PlaceCard";
    import BookingItem from "../../components/places/BookingItem";
    export default {
        name: "listings",
        layout: 'hosting',
        components: {BookingItem, PlaceCard},
        data: ()=> {
          return {
              working: true,
              created: false,
              places: []
          }
        },
        mounted() {
            this.$axios.get(this.$api.Place.List)
                .then( r => this.places = r.data )
        }
    }
</script>

<style scoped>

</style>