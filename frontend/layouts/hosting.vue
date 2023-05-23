<template>
    <v-app>
        <v-content>
            <HostingHeader/>

            <div class="UserDashboardContent">
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
    import HostingHeader from "../components/general/HostingHeader";
    import Alert from "../components/general/Alert";

    export default {
        name: "hosting",
        components: {Alert, HostingHeader, SiteFooter, SiteHeader}
    }
</script>

<style scoped>
    .UserDashboardContent {
        min-height: calc(100vh - 140px);
        /*background-color: #f2f3f8;*/
        border-bottom: 1px solid #eee;
    }
</style>
