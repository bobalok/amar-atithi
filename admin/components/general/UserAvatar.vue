<template>
    <div class="UserSmallAvatar d-inline-block" >

        <div class="UsaContent d-inline-block">
            <nuxt-link to="/">
                <v-avatar :size="size">
                    <img :src="avatar"/>
                </v-avatar>
            </nuxt-link>
        </div>
        <div class="UsaTooltipOutter">
            <div class="UsaTooltip">{{name}}</div>
        </div>

    </div>
</template>

<script>
    export default {
        name: "UserAvatar",
        props:['avatar', 'name', 'size']
    }
</script>

<style scoped>

</style>
