<template>
<div>
	<h3>
		Create an airing
	</h3>
	<form @submit.prevent="submitform">

		<p>
			<label for = "show"> Which show is going to air? </label>
			<select id="show" v-model="show_selected">
					<option v-for="show in this.$store.state.all_shows" :value="show.SID"> {{show.SNAME}} </option>
			</select>
		</p>
		
		<p>
			<label for="theatre"> Which of your theatres will it air in? </label>
			<select id="theatre" v-model="theatre_selected">
				<option v-for="theatre in this.$store.state.your_theatres" :value="theatre.TID"> {{theatre.TNAME}} </option>
			</select>
		</p>

		<p> 
			<label for="date"> On what day will it air? </label>
			<input type="date" id = "date" v-model="date" :formatter="date_format"/>
		</p>
		
		<p v-if="(date !== '') && (theatre_selected !== '') "> 
			<p>
				<label for="strt_time"> At what time will it start? </label>
				<input type="time" id="strt_time" v-model="strt_time" :formatter="time_format"> 
			</p>

			<p>
				<label for="stop_time"> At what time will it end? </label>
				<input type="time" id="stop_time" v-model="stop_time" :formatter="time_format"> 
			</p>

			<p>
				For your ready reference, here is a list of all the other shows airing in {{theatre_selected}} on {{date}} <br>
				<table class = "table">
					<thead>
						<tr>
							<th scope = "col"> # </th>
							<th scope = "col">Show Name </th>
							<th scope = "col"> At theatre </th>
							<th scope = "col"> Starts at </th>
							<th scope = "col"> Ends by </th>
							<th scope = "col"> Date </th>
	
						</tr>
					</thead>
					<tbody>
						<tr v-for="(airing, index) in airings_date_tid">
							<td> {{index+1}} </td>
							<td> {{airing.SNAME}} </td>
							<td> {{airing.TNAME}} </td>
							<td> {{airing.STRT_TIME}} </td>
							<td> {{airing.STOP_TIME}} </td>
							<td> {{airing.DATE}} </td>
						</tr>
						<br>
					</tbody>
				</table>
			</p>

			<p>
				<button type="submit"> Create airing</button>
			</p>
		</p>

	</form>

</div>
</template>

<script>
import store from '@/store/index.js'
import router from '@/router/index.js'

export default {
	name:'Makeairing_form',
	
	data(){
		return{
				show_selected:'',
				theatre_selected:'',
				your_theatres:[],
				all_shows:[],
				date:'',
				strt_time:'',
				stop_time:'',
				airings_date_tid:[]
			}
	},

	beforeCreate(){

		//fetching all the shows that exist
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
			console.log(this.all_shows)
			
			let payload = {'all_shows' : this.all_shows}
			store.commit('add_all_shows', payload) 
		})
		.catch((error) =>{
			console.error('Error: ', error)
		});

		// fetching theatres made by the current user
		fetch('http://192.168.148.107:8000/your_theatres_get',{
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
				this.your_theatres.push(data[i])
			
			let payload = {'your_theatres' : this.your_theatres}
			store.commit('add_your_theatres', payload)
			//console.log(this.$store.state.your_theatres)
		})
		.catch((error) =>{
			console.error('Error: ', error)
		});

		//fetching airings slated for the future

	},

	methods:{

	date_format(value, event){
		return moment(value).format('YYYY-MM-DD')
	},

	time_format(value,event){
		console.log()
		return moment(value).format('h:mm')
	},

	submitform(event){
			fetch('http://192.168.148.107:8000/airings_post',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token,
					'action': 'create'
					},
				body: JSON.stringify({"show_specific":this.show_selected, "theatre_specific":this.theatre_selected, "date":this.date, "strt_time":this.strt_time, "stop_time":this.stop_time})				})																				// this bracket is the end of fetch

			.then(response => response.json())

			.then(data => {
				console.log(data.msg);
				router.push({name:'Future_shows'})
				})																				//this bracket is the end of the then block

			.catch((error) => {
					console.error('Error: ', error)
				});																		
		},

	},

	watch: {

		date(new_val){
			if((new_val !== '')&&(this.theatre_selected !== '')){
				fetch('http://192.168.148.107:8000/get_airings_date_tid',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token,
					},
				body: JSON.stringify({'date':this.date, 'tid':this.theatre_selected})	})																				// this bracket is the end of fetch

				.then(response => response.json())

				.then(data => {
					this.airings_date_tid=[]
					for (var i in data)
						this.airings_date_tid.push(data[i]);
					//console.log(this.airings_date_tid)
					})																			//this bracket is the end of the then bloc

				.catch((error) => {
						console.error('Error: ', error)
					});	
			
			}
		},

		theatre_selected(new_val){
			if((new_val !== '') && (this.date !== '')){
				fetch('http://192.168.148.107:8000/get_airings_date_tid',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token,
					},
				body: JSON.stringify({'date':this.date, 'tid':this.theatre_selected})	})																				// this bracket is the end of fetch

				.then(response => response.json())

				.then(data => {
					this.airings_date_tid=[]
					for (var i in data)
						this.airings_date_tid.push(data[i]);
					//console.log(this.airings_date_tid)

				
					})																			//this bracket is the end of the then block

				.catch((error) => {
						console.error('Error: ', error)
					});	
			}
		}

	}

}
</script>

<style scoped>
	
</style>