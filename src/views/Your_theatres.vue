<template>
<div>
	<h3>
		You are now looking at the page with all the theatres you've made.
	</h3>
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
			<tr v-for="(theatre, index) in your_theatres">
				<td> {{index+1}} </td>
				<td> {{theatre.TNAME}} </td>
				<td> {{theatre.LOCATION}} </td>
				<td> {{theatre.CAPACITY}} </td>
				<td> <button v-on:click="edit_theatre(`${index}`)" > Modify Venue </button> </td>
				<td> <button v-on:click="delete_theatre(`${index}`)" > Delete Venue	 </button> </td>
			</tr>
			<br>
		</tbody>
	</table>
</div>
</template>

<script>
import store from '@/store/index.js'
import router from '@/router/index.js'

export default{
	name:'Your_theatres',
	data(){
		return{
			your_theatres: []
		}
	},

	mounted(){
		fetch('http://192.168.148.107:8000/your_theatres_get',{
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
				this.your_theatres.push(data[i])
			
			let payload = {'your_theatres' : this.your_theatres}
			store.commit('add_your_theatres', payload)
			//console.log(this.$store.state.your_theatres)
		})
		.catch((error) =>{
			console.error('Error: ', error)
		});
	},

	methods:{
		edit_theatre(index){
			router.push('/Modtheatre/'+String(index)+'/update')
		},
		delete_theatre(index){
			router.push('/Modtheatre/'+String(index)+'/delete')
		}
	}
}
</script>

<style scoped>
</style>