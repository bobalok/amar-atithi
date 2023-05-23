<template>
    
</template>

<script>
    export default {
        name: "logout",
        mounted() {
            if( this.$auth.loggedIn ){
                this.$auth.logout()
            } else {
                this.$router.push("/")
            }
        }
    }
</script>

<style scoped>

</style>
