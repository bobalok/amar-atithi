<template>
    <div>
        <v-snackbar
                :value="IonSnack.show"
                :bottom="IonSnack.bottom"
                :left="IonSnack.left"
                :multi-line="IonSnack.multi"
                :right="IonSnack.right"
                :timeout="3000"
                :top="IonSnack.top"
                :vertical="IonSnack.v"
                :color="IonSnack.color"
        >
            {{ IonSnack.text }}
            <v-btn
                    dark
                    text
                    @click="Close"
            >
                Dismiss
            </v-btn>
        </v-snackbar>


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
                            class="pull-right">{{button.text}}
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
    </div>
</template>


<script>

    export default {
        name: "Alert",
        computed: {
            IonDialogue() {
                return this.$store.state.alert.IonDialogue
            },
            IonSnack: {
                get() {
                    return this.$store.state.alert.IonSnack
                },
                set(value) {
                    this.$store.commit('alert/SetIonSnack', value)
                }
            }
        },
        methods: {
            Close() {
                this.$store.commit("alert/CloseSnack")
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
