<template>
    <v-app>
        <template v-if="error.statusCode === 404">
            <div class="page-header mb-3">
                <div class="subheader-main">
                    <h3>Not Found</h3>
                </div>
            </div>

            <p>Sorry but you are looking for a page that doesn't exists or restricted. <nuxt-link to="/">Return to dashboard.</nuxt-link></p>
        </template>
        <template v-else>
            {{error}}
        </template>
    </v-app>
</template>

<script>
    export default {
        layout: 'empty',
        props: {
            error: {
                type: Object,
                default: null
            }
        },
        head() {
            const title =
                this.error.statusCode === 404 ? this.pageNotFound : this.otherError
            return {
                title
            }
        },
        data() {
            return {
                pageNotFound: '404 Not Found',
                otherError: 'An error occurred'
            }
        }
    }
</script>

<style scoped>
    h1 {
        font-size: 20px;
    }
</style>
