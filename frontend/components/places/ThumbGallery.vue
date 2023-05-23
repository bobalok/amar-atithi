<template>
    <div class="place-images-gallery">

        <v-container fill-height class="pt-0 pb-0" fluid>
            <v-layout wrap row>

                <v-flex :class="{xs6: images.length > 1, xs12: images.length == 1}">

                    <v-img
                            :src="images[0]['file']"
                            :lazy-src="require(`@/assets/media/lazy-placeholder.jpg`)"
                            aspect-ratio="1.5"
                            class="grey lighten-2"
                    >
                        <template v-slot:placeholder>
                            <v-row
                                    class="fill-height ma-0"
                                    align="center"
                                    justify="center"
                            >
                                <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                            </v-row>
                        </template>
                    </v-img>
                </v-flex>

                <v-flex v-if="images.length > 1" xs6>
                    <v-layout class="fill-height" column wrap>
                        <v-flex :class="{xs6: images.length > 2, xs12: images.length == 2}">
                            <v-img
                                    :src="images[1]['file']"
                                    :lazy-src="require(`@/assets/media/lazy-placeholder.jpg`)"
                                    aspect-ratio="3"
                                    class="grey lighten-2"
                            >
                                <template v-slot:placeholder>
                                    <v-row
                                            class="fill-height ma-0"
                                            align="center"
                                            justify="center"
                                    >
                                        <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                                    </v-row>
                                </template>
                            </v-img>
                        </v-flex>

                        <v-flex v-if="images.length > 2" xs6>
                            <v-container fill-height class="pt-0 pb-0" fluid>
                                <v-layout row wrap>
                                    <v-flex :class="{xs6: images.length > 3, xs12: images.length == 3}">
                                        <v-img
                                                :src="images[2]['file']"
                                                :lazy-src="require(`@/assets/media/lazy-placeholder.jpg`)"
                                                :aspect-ratio="images.length == 3 ? 3: 1.5"
                                                class="grey lighten-2"
                                        >
                                            <template v-slot:placeholder>
                                                <v-row
                                                        class="fill-height ma-0"
                                                        align="center"
                                                        justify="center"
                                                >
                                                    <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                                                </v-row>
                                            </template>
                                        </v-img>
                                    </v-flex>

                                    <v-flex xs6 v-if="images.length > 3">
                                        <v-img
                                                :src="images[3]['file']"
                                                :lazy-src="require(`@/assets/media/lazy-placeholder.jpg`)"
                                                aspect-ratio="1.5"
                                                class="grey lighten-2"
                                        >
                                            <template v-slot:placeholder>
                                                <v-row
                                                        class="fill-height ma-0"
                                                        align="center"
                                                        justify="center"
                                                >
                                                    <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                                                </v-row>
                                            </template>
                                        </v-img>
                                    </v-flex>
                                </v-layout>
                            </v-container>
                        </v-flex>
                    </v-layout>
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
    export default {
        name: "ThumbGallery",
        props: ['images']
    }
</script>

<style lang="scss" scoped>


    .gallery-image {
        width: 100%;
        height: 100%;
        background-size: cover;
        background-position: center center;
    }
</style>