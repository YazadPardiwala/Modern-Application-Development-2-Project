<template>
<div>
	<div>
		You have currently booked tickets for the following show airings:
		<table class = "table">
		<thead>
			<tr>
				<th scope = "col"> # </th>
				<th scope = "col">Show Name </th>
				<th scope = "col"> Starting at </th>
				<th scope = "col"> Ending by </th>
				<th scope = "col"> On </th>
				<th scope = "col"> Ticket number </th>
				<th scope = "col"> At this theatre </th>
			</tr>
		</thead>
		<tbody>
			<tr v-for="(show, index) in booked_shows">
				<td> {{index+1}} </td>
				<td> {{show.SNAME}} </td>
				<td> {{show.STRT_TIME}} </td>
				<td> {{show.STOP_TIME}} </td>
				<td> {{show.DATE}} </td>
				<td> {{show.TICKETS}} </td>
				<td> {{show.TNAME}} </td>
			</tr>
			<br>
		</tbody>
	</table>
	</div>
</div>
</template>


<script>
import store from '@/store/index.js'

export default{
	name: 'Booked_shows',

	data(){
	return{
		booked_shows:[]
		}
	},

	mounted() {
		fetch('http://192.168.148.107:8000/bookings_get',{
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
				this.booked_shows.push(data[i])
		})
		.catch((error) =>{
			console.error('Error: ', error)
		});
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