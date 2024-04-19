<template>
<div>
	<h3>
		You may now create a theatre my son
	</h3>
	<form @submit.prevent="submitform">
		<p>
			<label for="name">Name:</label> <br>
			<input type="text" id="name" v-model='name'>
		</p>
		<p>
			<label for="capacity"> Capacity: </label> <br>
			<input type="number" id="capacity" v-model='capacity'>
		</p>
		<p>
			<label for="location"> Location: </label> <br>
			<input type="text" id="location" v-model="location">
		</p>
		<p>
			<button type="submit">Submit</button> 
		</p>
	</form>
</div>
</template>

<script>
import store from '@/store/index.js'
import router from '@/router/index.js'

export default {
	name:'Maketheatre_form',
	
	data(){
		return{
				name:'',
				capacity:0,
				location:'',
				action:'create'
			}
	},

	methods:{
	submitform(event){
			fetch('http://192.168.148.107:8000/theatre_post',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token,
					'action': this.action
					},
				body: JSON.stringify({'name':this.name, 'capacity':this.capacity, 'location':this.location}),
				})																				// this bracket is the end of fetch

			.then(response => response.json())

			.then(data => {
				console.log(data.msg);
				router.push({name:'Your_theatres'})
				})																				//this bracket is the end of the then block

			.catch((error) => {
					console.error('Error: ', error)
				});																				//these brackets are the end of the try blcok
		},
	}
}
</script>

<style scoped>
</style>