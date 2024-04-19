<template>
<div>

	<div>
	<form @submit.prevent="submitform">
		<h3>
			<label for="search_val"> Type the name/Location of theatre(s) you want: </label> <br>
			<input type="text" id="search_val" v-model="search_val">
			<button type="submit">Search?</button> 
		</h3>
	</form>
	</div>

	<div v-if="search == false">
		You are now looking at the page with all theatres 
		<table class = "table">
			<thead>
				<tr>
					<th scope = "col"> # </th>
					<th scope = "col">Theatre Name </th>
					<th scope = "col"> Address </th>
					<th scope = "col"> Capacity </th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="(theatre, index) in all_theatres">
					<td> {{index+1}} </td>
					<td> {{theatre.TNAME}} </td>
					<td> {{theatre.LOCATION}} </td>
					<td> {{theatre.CAPACITY}} </td>
				</tr>
				<br>
			</tbody>
		</table>
	</div>

	<div v-if="search == true">
		This will eventually let you see just what you looked for
		<table class = "table">
			<thead>
				<tr>
					<th scope = "col"> # </th>
					<th scope = "col">Theatre Name </th>
					<th scope = "col"> Address </th>
					<th scope = "col"> Capacity </th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="(theatre, index) in specific_theatres">
					<td> {{index+1}} </td>
					<td> {{theatre.TNAME}} </td>
					<td> {{theatre.LOCATION}} </td>
					<td> {{theatre.CAPACITY}} </td>
				</tr>
				<br>
			</tbody>
		</table>
		<div>
			<button @click="revert"> Go back to the list of all theatres? </button>
		</div>
	</div>
</div>
</template>



<script>
import store from '@/store/index.js'
import router from '@/router/index.js'

export default{
	name: 'All_theatres',
	data(){
		return{
			all_theatres: [],
			specific_theatres: [],
			search_val:'',
			search:false
		}
	},

	beforeMount(){

		this.specific_theatres = this.$store.state.specific_theatres
		this.search = this.$store.state.theatre_searched
		//console.log(this.specific_theatres)

		fetch('http://192.168.148.107:8000/all_theatres_get',{
			method:'GET',
			headers:{
					'login-token': this.$store.state.token,
					'user_curr': this.$store.state.user_curr
				}
		})
		.then(response => response.json())
		.then(data => {
			//console.log(data);
			
			for (var i in data)
				this.all_theatres.push(data[i])
			//console.log(this.all_theatres)
			
			let payload = {'all_theatres' : this.all_theatres}
			store.commit('add_all_theatres', payload) 
			//console.log(this.$store.state.all_theatres)
		})
		.catch((error) =>{
			console.error('Error: ', error)
		});
	},

	methods:{
	submitform(event){
			this.search=true
			console.log(this.search)

			fetch('http://192.168.148.107:8000/specific_theatres_get',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token,
					},
				body: JSON.stringify({'search_val':this.search_val}),
				})																				// this bracket is the end of fetch

			.then(response => response.json())

			.then(data => {
				this.specific_theatres=[]
				for (var i in data)
					this.specific_theatres.push(data[i]);

				let payload = {'specific_theatres' : this.specific_theatres}
				store.commit('add_specific_theatres', payload)
				console.log(this.$store.state.specific_theatres)

				})																			//this bracket is the end of the then bloc
			.catch((error) => {
					console.error('Error: ', error)
				});																				//these brackets are the end of the try blcok
		},
	
	revert(event){
			this.search=false
			store.commit('remove_specific_theatres')
		},
	}

}
</script>

<style scoped>
input{
	margin-top:10px
}
</style>