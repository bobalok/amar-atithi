<template>
    <v-dialog v-model="IonDialogue.show" persistent max-width="600">
        <div class="IonDialogue">
            <div class="IonDHeader">
                <h2 class="HeaderTitle">{{IonDialogue.title}}</h2>
            </div>

            <div class="IonDBody" v-html="IonDialogue.content"></div>

            <div v-if="IonDialogue.buttons" class="IonDFooter">
                <v-btn v-if="!IonDialogue.NoCancel" @click="IonDialogue.show = false" :block="$vuetify.breakpoint.xsOnly" color="blue-grey lighten-5" class="IonDBtn mb-2">{{IonDialogue.hasOwnProperty("cancelText") ? IonDialogue.cancelText : "Cancel" }}</v-btn>
                <v-btn v-for="button in IonDialogue.buttons" :key="button.text" :block="$vuetify.breakpoint.xsOnly" @click="button.action" color="primary" class="IonDBtn right mb-2">{{button.text}}</v-btn>
            </div>
            <div v-else class="IonDFooter">
                <v-btn @click="IonDialogue.show = false"  color="primary" :block="$vuetify.breakpoint.xsOnly" class="IonDBtn right mb-2">{{IonDialogue.hasOwnProperty("cancelText") ? IonDialogue.cancelText : "Cancel" }}</v-btn>
            </div>
        </div>
    </v-dialog>
</template>


<script>

    export default {
        name: "IonDialogue",
        computed: {
            IonDialogue: {
                get() {
                    return this.$store.state.alert.IonDialogue
                },
                set(value) {
                    this.$store.commit('alert/SetIonDialogue', value)
                }
            },
        },
        data: () => {
            return {
                title: "IonDialogue",
            }
        }
    }
</script>


<style scoped>

</style>
