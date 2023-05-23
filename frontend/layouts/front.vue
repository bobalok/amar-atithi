<template>
    <v-app>
        <v-content>
            <nuxt/>

            <SiteFooter/>
        </v-content>
    </v-app>
</template>

<script>
    import SiteFooter from "../components/general/SiteFooter";
    export default {
        name: "front",
        components: {SiteFooter},
        mounted() {


        }
    }
</script>

<style scoped>

</style>
