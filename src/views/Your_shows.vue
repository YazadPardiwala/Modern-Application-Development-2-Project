<template>
<div>
	<h3>
		Here are all of the shows you've made.
	</h3>
	<table class = "table">
		<thead>
			<tr>
				<th scope = "col"> # </th>
				<th scope = "col">Show Name </th>
				<th scope = "col"> Description </th>
				<th scope = "col"> Price </th>
				<th scope = "col"> Rating </th>
				<th scope = "col"> Tags </th>
			</tr>
		</thead>
		<tbody>
			<tr v-for="(show, index) in your_shows">
				<td> {{index+1}} </td>
				<td> {{show.SNAME}} </td>
				<td> <textarea> {{show.S_DESCR}} </textarea> </td>
				<td> {{show.PRICE}} </td>
				<td> {{show.RATING_AGG}} </td>
				<td> {{show.S_TAGS}} </td>
				<td> <button v-on:click="edit_show(`${index}`)" > Modify </button> </td>
				<td> <button v-on:click="delete_show(`${index}`)" > Delete Show</button> </td>
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
	name:'Your_shows',
	data(){
		return{
			your_shows: []
		}
	},

	mounted(){
		fetch('http://192.168.148.107:8000/your_shows_get',{
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
				this.your_shows.push(data[i])
			
			let payload = {'your_shows' : this.your_shows}
			store.commit('add_your_shows', payload)
			//console.log(this.$store.state.your_shows)
		})
		.catch((error) =>{
			console.error('Error: ', error)
		});
	},

	methods:{
		edit_show(index){
			router.push('/Modshow/'+String(index)+'/update')
		},
		delete_show(index){
			router.push('/Modshow/'+String(index)+'/delete')
		}
	}
}
</script>

<style scoped>
</style>