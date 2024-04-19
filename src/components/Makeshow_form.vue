<template>
<div>
	<h3>
		Create a show
	</h3>
	<form @submit.prevent="submitform">
		<p>
			<label for="name">Name:</label> <br>
			<input type="text" id="name" v-model='name'>
		</p>
		<p>
			<label for="s_descr"> Description: </label> <br>
			<input type="text" id="s_descr" v-model='s_descr'>
		</p>
		<p>
			<label for="price"> Price: </label> <br>
			<input type="number" id="price" v-model='price'>
		</p>
		<p>
			<label for="s_tags"> Tags: </label> <br>
			<input type="text" id="s_tags" v-model='s_tags'>
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
	name:'Makeshow_form',
	
	data(){
		return{
				name:'',
				price:0,
				s_descr:'',
				s_tags:'',
				action:'create'
			}
	},

	methods:{
	submitform(event){
			fetch('http://192.168.148.107:8000/show_post',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token,
					'action': this.action
					},
				body: JSON.stringify({'name':this.name, 'price':this.price, 's_descr':this.s_descr, 's_tags':this.s_tags}),
				})																				// this bracket is the end of fetch

			.then(response => response.json())

			.then(data => {
				console.log(data.msg);
				router.push({name:'Your_shows'})
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