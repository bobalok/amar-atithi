<template>
    <v-app>
        <v-content>
            <SiteHeader/>

            <div class="MainContent">
                <nuxt/>
            </div>

            <Alert/>
            <SiteFooter/>
        </v-content>
    </v-app>
</template>

<script>
    import SiteHeader from "../components/general/SiteHeader";
    import SiteFooter from "../components/general/SiteFooter";
    import Alert from "../components/general/Alert";
    export default {
        components: {Alert, SiteFooter, SiteHeader}
    }
</script>

<style scoped>
    .MainContent {
        min-height: calc(100vh - 140px);
    }
</style>
