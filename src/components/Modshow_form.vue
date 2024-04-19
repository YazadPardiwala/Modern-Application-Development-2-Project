<template>
<div>
	<div v-if="$route.params.ACTION === 'update'">
		<h3>
			You may now modify the below show
		</h3>
		<form @submit.prevent="submitform">
			<p>
				<label for="name">Name:</label> <br>
				<input type="text" id="name" v-model='show.SNAME'>
			</p>
			<p>
				<label for="s_descr"> Description: </label> <br>
				<input type="text" id="s_descr" v-model='show.S_DESCR'>
			</p>
			<p>
				<label for="price"> Price: </label> <br>
				<input type="number" id="price" v-model='show.PRICE'>
			</p>
			<p>
				Rating_ Agg : {{show.RATING_AGG}}	
			</p>
			<p>
				<label for="tags"> Tags: </label> <br>
				<input type = "text" id="tags" v-model='show.S_TAGS'>
			</p>
			<p>
				<button type="submit">Submit</button> 
			</p>
		</form>
	</div>

	<div v-if="$route.params.ACTION === 'delete'">
		<h3>
			Are you sure you want to delete this Show?
		</h3>
		<form @submit.prevent="submitform">
			<table class = "table">
				<thead>
					<tr>
						<th scope = "col">Show details </th>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td> Name </td>
						<td> {{show.SNAME}} </td>
					</tr>
					<tr>
						<td> Name </td>
						<td> {{show.S_DESCR}} </td>
					</tr>
					<tr>
						<td> Price </td>
						<td> {{show.PRICE}} </td>
					</tr>
					<tr>
						<td> Rating </td>
						<td> {{show.RATING_AGG}} </td>
					</tr>
					<tr>
						<td> Tags </td>
						<td> {{show.S_TAGS}} </td>
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
	name:'Modshow_form',

	data(){
		return{
				show:{},
				action:this.$route.params.ACTION
			}
	},

	beforeMount(){
		this.show = this.$store.state.your_shows[this.$route.params.SID]
	},

	methods: {
		submitform(event){
			fetch('http://192.168.148.107:8000/show_post',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token,
					'action': this.action
					},
				body: JSON.stringify({'sid':this.show.SID, 'name':this.show.SNAME, 'price':this.show.PRICE, 's_descr':this.show.S_DESCR}),
				})																				// this bracket is the end of fetch

			.then(response => response.json())

			.then(data => {
				console.log(data.msg);
				router.push({name:'Your_shows'})
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