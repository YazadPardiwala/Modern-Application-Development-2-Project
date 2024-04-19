import { createStore } from 'vuex'

export default createStore({
  state: {
	token: 0,
	user_curr: -1,
	admin: 0,

	future_airings: [],
	your_airings:[],

	your_theatres: [],
	all_theatres: [],
	specific_theatres: [],
	theatre_searched: false,

	your_shows: [],
	all_shows: [],
	specific_shows: [],
	show_searched: false,
  },

  getters: {
  },

  mutations: {
	login(state, payload) {
		state.token = payload.login_token;
		state.user_curr = payload.user_curr
		state.admin = payload.admin
	},

	add_future_airings(state,payload) {
		state.future_airings = payload.future_shows
	},
	add_your_airings(state,payload){
		state.your_airings = payload.your_airings
	},

	add_your_theatres(state,payload){
		state.your_theatres = payload.your_theatres
	},
	add_all_theatres(state,payload){
		state.all_theatres = payload.all_theatres
	},
	add_specific_theatres(state,payload){
		state.specific_theatres = payload.specific_theatres;
		state.theatre_searched = true
	},
	remove_specific_theatres(state){
		state.specific_theatres = [];
		state.theatre_searched = false
	},

	add_your_shows(state,payload){
		state.your_shows = payload.your_shows
	},
	add_all_shows(state,payload){
		state.all_shows = payload.all_shows
	},
	add_specific_shows(state, payload){
		state.specific_shows = payload.specific_shows;
		state.show_searched = true
	},
	remove_specific_shows(state){
		state.specific_shows = [];
		state.show_searched = false
	}

  },

  actions: {
  },

  modules: {
  }
})
