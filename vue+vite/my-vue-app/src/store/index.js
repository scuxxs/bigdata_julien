import{ createStore } from 'vuex'
export default  createStore({
    state:{
        isCollapse:true,
        panelData: {
            academicWarning: [],
            lateWarning: [],
            psychologicalWarning: [],
            povertyWarning: [],
            cheatWarning: [],
            politicsWarning: [],
            cheatLevel:[],
            mentalLevel:[],
            povertyLevel:[],
            politicsLevel:[],
            lateLevel:[],
            academicLevel:[],
        },
    },
    mutations:{
        updateIsCollapse(state,payload){
    state.isCollapse =!state.isCollapse
        },
        updatePanelContent(state, data) {
            state.panelData = data;
        },
        }
})

