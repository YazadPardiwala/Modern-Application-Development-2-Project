<template>
<div>
	<form @submit.prevent="book_airing">
		<table class = "table">
			<thead>
				<tr>
					<th scope = "col"> Book a show </th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td> Name: </td>
					<td> {{Airing.SNAME}} </td>
				</tr>			
				<tr>
					<td> Starts at </td>
					<td> {{Airing.STRT_TIME}} </td>
				</tr>
				<tr>
					<td> Ends by </td>
					<td> {{Airing.STOP_TIME}} </td>
				</tr>
				<tr>
					<td> Cost: </td>
					<td> {{Airing.PRICE}} </td>
				</tr>
				<tr>
					<td> Rated </td>
					<td> {{Airing.RATING_AGG}} </td>
				</tr>
				<tr>
					<td> Airs at </td>
					<td> {{Airing.TNAME}} </td>
				</tr>
				<tr>
					<td> Number of tickets :   </td>
					<td> <input type="number" v-model='Tickets'>  </td>
				</tr>
				<tr v-if="!this.msg">
					<button type="submit"> Book? </button>
				</tr>
			</tbody>
		</table>
		<h4>
			{{msg}}
		</h4>
	</form>
</div>
</template>

<script>
import store from '@/store/index.js'
import router from '@/router/index.js'

export default {
  name: 'Show_book_form',

  data(){
	return{
		Airing:{},
		Tickets:1,
		aid:0
		}
	},

  beforeMount(){
		this.Airing = this.$store.state.future_airings[this.$route.params.AID];
		
	},

	methods:{
		book_airing(){
			fetch('http://192.168.148.107:8000/bookings_post',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token
					},
				body: JSON.stringify({'AID': this.$route.params.AID , 'Tickets':this.Tickets , 'SID':this.Airing.SID , 'TID':this.Airing.TID }),
				})																				// this bracket is the end of fetch

			.then(response => response.json())

			.then(data => {
				//console.log(data.msg);
				})																				//this bracket is the end of the then block

			.catch((error) => {
					console.error('Error: ', error)
				});																				//these brackets are the end of the try blcok

				router.push('/Booked_shows')
		}
	},

	computed: {
		msg(){
			if (this.Tickets > this.Airing.VACANCIES){
				return `Please, we only have ${this.Airing.VACANCIES} tickets. You can't order more than that. Reduce to at most ${this.Airing.VACANCIES} tickets and we'll let you book your tickets.`
			}
		}
	}
  }
  
</script>

<style scoped>
</style>