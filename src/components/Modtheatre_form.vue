<template>
<div>
	<div v-if="$route.params.ACTION === 'update'">
		<h3>
			You may now modify the below theatre 
		</h3>
		<form @submit.prevent="submitform">
			<p>
				<label for="name">Name:</label> <br>
				<input type="text" id="name" v-model='theatre.TNAME'>
			</p>
			<p>
				<label for="capacity"> Capacity: </label> <br>
				<input type="number" id="capacity" v-model='theatre.CAPACITY'>
			</p>
			<p>
				<label for="location"> Location: </label> <br>
				<input type="text" id="location" v-model="theatre.LOCATION">
			</p>
			<p>
				<button type="submit">Submit</button> 
			</p>
		</form>
	</div>

	<div v-if="$route.params.ACTION === 'delete'">
		<h3>
			Are you sure you want to delete this theatre?
		</h3>
		<form @submit.prevent="submitform">
			<table class = "table">
				<thead>
					<tr>
						<th scope = "col">Theatre details </th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td> Name </td>
						<td> {{theatre.TNAME}} </td>
					</tr>
					<tr>
						<td> Location </td>
						<td> {{theatre.LOCATION}} </td>
					</tr>
					<tr>
						<td> Capacity </td>
						<td> {{theatre.CAPACITY}} </td>
					</tr>
					<tr>
						<button type="submit"> Yes </button>
					</tr>
					<br>
				</tbody>
			</table>
		</form>
	</div>
</div>
</template>

<script>
import store from '@/store/index.js'
import router from '@/router/index.js'

export default {
	name:'Modtheatre_form',

	data(){
		return{
				theatre:{},
				action:this.$route.params.ACTION
			}
	},

	beforeMount(){
		this.theatre = this.$store.state.your_theatres[this.$route.params.TID]
	},

	methods: {
		submitform(event){
			fetch('http://192.168.148.107:8000/theatre_post',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token,
					'action': this.action
					},
				body: JSON.stringify({'tid':this.theatre.TID, 'name':this.theatre.TNAME, 'capacity':this.theatre.CAPACITY, 'location':this.theatre.LOCATION}),
				})																				// this bracket is the end of fetch

			.then(response => response.json())

			.then(data => {
				console.log(data.msg);
				router.push({name:'Your_theatres'})
				})																				//this bracket is the end of the then block

			.catch((error) => {
					console.error('Error: ', error)
				});																				//these brackets are the end of the try blcok
		}
	}


}
</script>

<style scoped>
</style>