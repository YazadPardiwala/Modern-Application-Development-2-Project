<template>
<div>
	<h3>
		Here are all of the upcoming airings you've made.
	</h3>
	<table class = "table">
		<thead>
			<tr>
				<th scope = "col"> # </th>
				<th scope = "col">Show</th>
				<th scope = "col">Theatre </th>
				<th scope = "col"> Starting at </th>
				<th scope = "col"> Ending by</th>
				<th scope = "col"> Date</th>
			</tr>
		</thead>
		<tbody>
			<tr v-for="(airing, index) in your_airings">
				<td> {{index+1}} </td>
				<td> {{airing.SNAME}} </td>
				<td> {{airing.TNAME}} </td>
				<td> {{airing.STRT_TIME}} </td>
				<td> {{airing.STOP_TIME}} </td>
				<td> {{airing.DATE}} </td>
				<td> <button v-on:click="edit_airing(`${index}`)" > Modify </button> </td>
				<td> <button v-on:click="delete_airing(`${index}`)" > Delete airing</button> </td>
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
	name:'Your_airings',
	data(){
		return{
			your_airings: []
		}
	},

	mounted(){
		fetch('http://192.168.148.107:8000/your_airings_get',{
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
				this.your_airings.push(data[i])
	
			let payload = {'your_airings' : this.your_airings}
			store.commit('add_your_airings', payload)
			console.log(this.$store.state.your_airings)
		})

		.catch((error) =>{
			console.error('Error: ', error)
		});
	},

	methods:{
		edit_airing(index){
			router.push('/Modairing_form/'+String(index)+'/update')
		},
		delete_airing(index){
			router.push('/Modairing_form/'+String(index)+'/delete')
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