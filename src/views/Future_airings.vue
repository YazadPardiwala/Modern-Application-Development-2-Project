<template>
<div>
	<h3>
		Below are all of the details of all shows airing in the near future
	</h3>
	<table class = "table">
		<thead>
			<tr>
				<th scope = "col"> # </th>
				<th scope = "col">Show Name </th>
				<th scope = "col"> At theatre </th>
				<th scope = "col"> Starts at </th>
				<th scope = "col"> Ends by </th>
				<th scope = "col"> Date </th>
				<th scope = "col"> Price </th>
				<th scope = "col"> Vacancies </th>
				<th scope = "col"> Rating </th>
			</tr>
		</thead>
		<tbody>
			<tr v-for="(Show, index) in future_shows" :key="Show">
				<td> {{index+1}} </td>
				<td> {{Show.SNAME}} </td>
				<td> {{Show.TNAME}} </td>
				<td> {{Show.STRT_TIME}} </td>
				<td> {{Show.STOP_TIME}} </td>
				<td> {{Show.DATE}} </td>
				<td> {{Show.PRICE}} </td>
				<td> {{Show.VACANCIES}} </td>
				<td> {{Show.RATING_AGG}} </td>
				<td> <button v-on:click="redirect_book(`${index}`)" > Book </button> </td>
			</tr>
			<br>
		</tbody>
	</table>
</div>
</template>

<script>
import store from '@/store/index.js'
import router from '@/router/index.js'

export default {
name:'Future_shows',

data(){
	return{
		future_shows:[],
		all_shows:[],
		all_theatres:[]
		}
	},

components: {
},

beforeMount() {
		fetch('http://192.168.148.107:8000/future_airings_get',{
			method:'GET',
			headers:{
					'login-token': this.$store.state.token,
					'user_curr': this.$store.state.user_curr,
				}
		})
		.then(response => response.json())
		.then(data => {
			//console.log(data);
			
			for (var i in data)
				this.future_shows.push(data[i])
			//console.log(this.future_shows)
			let payload = {'future_shows' : this.future_shows}
			store.commit('add_future_airings', payload)
			//console.log(this.$store.state.future_airings)
		})
		.catch((error) =>{
			console.error('Error: ', error)
		});
	},
	
	mounted(){
		
		//fetching all shows
		fetch('http://192.168.148.107:8000/all_shows_get',{
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
				this.all_shows.push(data[i])
			//console.log(this.all_shows)
			
			let payload = {'all_shows' : this.all_shows}
			store.commit('add_all_shows', payload) 
			//console.log(this.$store.state.all_shows)
		})
		.catch((error) =>{
			console.error('Error: ', error)
		});

		//fetching all theatres
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

	methods: {
		redirect_book(index){
			router.push('/Show_book/'+String(index))
		}
	}
}	
</script>

<style scoped>

tr{
    border: 1px solid;
}
th {
	border: 0px;
}

</style>