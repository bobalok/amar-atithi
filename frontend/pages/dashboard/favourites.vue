<template>
    <v-container>
        <div class="page-header d-flex mt-6 mb-4">
            <h1 class="section-title">Your Favourite Places</h1>
        </div>

        <div class="place-list">
            <div class="no-place" v-if="places.length == 0 ">You haven't add any places to your favourite list.</div>
        </div>
    </v-container>
</template>

<script>
    export default {
        name: "favourites",
        layout: 'dashboard',
        data: ()=> {
            return {
                places: []
            }
        }
    }
</script>

<style scoped>

</style>