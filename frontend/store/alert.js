export const state = () => ({
    IonDialogue: {
        show: false
    },
    IonSnack: {
        show: false
    }
})

export const mutations = {
    SetIonDialogue(state, value) {
        state.IonDialogue = value
    },
    CloseIonDialogue(state) {
        state.IonDialogue.show = false
    },
    SetIonSnack(state, value) {
        state.IonSnack = value
    },
    CloseSnack(state) {
        state.IonSnack.show = false
    },

}

export const actions = {
    SetSnack({commit, state}, value) {

        let defaultValue = {
            color: 'success',
            text: "Success",
            show: true,
            right: true,
            bottom: true
        }


        if (state.IonSnack.show) {
            commit('CloseSnack')
            setTimeout(() => {
                commit('SetIonSnack', Object.assign(defaultValue, value))
            }, 200)
        } else {
            commit('SetIonSnack', Object.assign(defaultValue, value))
        }
    },

    Snack({commit, state, dispatch }, value){
        let data = {
            color: 'success',
            text: value,
            show: true,
            right: true,
            bottom: true
        }

        dispatch("SetSnack", data)
    },
    ErrorSnack({commit, state, dispatch }, value){
        let msg = value == undefined || value == null || value.length ==0 ? 'Something went wrong. Please try again later' : value
        let data = {
            color: 'error',
            text: msg,
            show: true,
            right: true,
            bottom: true
        }

        dispatch("SetSnack", data)
    },


}
