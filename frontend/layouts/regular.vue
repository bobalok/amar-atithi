<template>
    <v-app>
        <v-content>
            <SiteHeader/>

            <nuxt/>

            <SiteFooter/>
        </v-content>
    </v-app>
</template>

<script>
    import SiteHeader from "../components/general/SiteHeader";
    import SiteFooter from "../components/general/SiteFooter";
    export default {
        name: "regular",
        components: {SiteFooter, SiteHeader}
    }
</script>

<style scoped>

</style>
