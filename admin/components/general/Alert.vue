<template>


    <v-dialog v-model="IonDialogue.show" persistent max-width="600">
        <div class="IonModal white">
            <div class="ModalHeader">
                <h3 class="modal-title">{{IonDialogue.title}}</h3>
            </div>

            <div class="ModalBody pa-4" v-html="IonDialogue.content"></div>

            <div v-if="IonDialogue.buttons" class="ModalFooter">
                <v-btn
                        v-if="!IonDialogue.NoCancel"
                        @click="Close"
                        :disabled="IonDialogue.disabled"
                        :block="$vuetify.breakpoint.xsOnly"
                        color="blue-grey lighten-5"
                        class="left">{{IonDialogue.hasOwnProperty("cancelText") ? IonDialogue.cancelText : "Cancel" }}
                </v-btn>

                <v-btn
                        v-for="button in IonDialogue.buttons"
                        :key="button.text"
                        :disabled="IonDialogue.disabled"
                        :loading="IonDialogue.disabled"
                        :block="$vuetify.breakpoint.xsOnly"
                        @click="button.action"
                        color="primary"
                        class="right">{{button.text}}
                </v-btn>
            </div>

            <div v-else class="ModalFooter">
                <v-btn
                        @click="Close"
                        color="primary"
                        :block="$vuetify.breakpoint.xsOnly"
                        class="active-flat right ma-0">{{IonDialogue.hasOwnProperty("cancelText") ? IonDialogue.cancelText : "Cancel" }}
                </v-btn>
            </div>
        </div>
    </v-dialog>
</template>


<script>

    export default {
        name: "IonDialogue",
        computed: {
            IonDialogue() {
                return this.$store.state.alert.IonDialogue
            }
        },
        methods: {
            Close() {
                this.$store.dispatch("alert/Close")
            }
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
