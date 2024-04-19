//HELLO FUTURE ME. PLS NOTE. CODE COPIED FROM MAKESHOW_FORM. NEEDS TO BE THOROUGHLY MODIFIED. ITS ONLY HERE TO GIVE YOU THE BROAD IDEA

<template>
<div>
	<div v-if="$route.params.ACTION === 'update'">
		<h3>
			You can modify the below airing
		</h3>
		<form @submit.prevent="submitform">

			<p>
				<label for = "show"> Show:-</label>
				<select id="show" v-model="show_selected">
						<option value=""> {{this.airing.SNAME}} </option>
						<option v-for="show in this.$store.state.all_shows" :value="show.SID"> {{show.SNAME}} </option>
				</select>
			</p>

			<p>
				<label for="theatre"> Theatre:- </label>
				<select id="theatre" v-model="theatre_selected">
					<option value=""> {{this.airing.TNAME}} </option>
					<option v-for="theatre in this.$store.state.your_theatres" :value="theatre.TID"> {{theatre.TNAME}} </option>
				</select>
			</p>

			<p> 
				<label for="date"> Date:- </label>
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
			</p>
			<p>
				<button type="submit">Submit</button> 
			</p>
		</form>
	</div>


	<div v-if="$route.params.ACTION === 'delete'">
		<h3>
			Are you sure you want to delete this Airing?
		</h3>
		<form @submit.prevent="submitform">
			<table class="table">
				<thead>
					<tr>
						<td class="col">Airing particulars </td>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>Show </td>
						<td>{{airing.SNAME}} </td>
					</tr>
					<tr>
						<td>Airing at theatre </td>
						<td>{{airing.TNAME}} </td>
					</tr>
					<tr>
						<td>On </td>
						<td>{{airing.DATE}} </td>
					</tr>
					<tr>
						<td>From </td>
						<td>{{airing.STRT_TIME}} </td>
					</tr>
					<tr>
						<td>To </td>
						<td>{{airing.STOP_TIME}} </td>
					</tr>
					<tr>
						<button type="submit"> Yes I'm sure </button>
					</tr>
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
	name:'Modairing_form',

	data(){
		return{
				airing:{},
				action:this.$route.params.ACTION,
				show_selected:'',
				theatre_selected:'',
				date:'',
				strt_time:'',
				stop_time:'',
				your_theatres:[],
				airings_date_tid:[],
			}
	},

	beforeMount(){

		//initializing all variables to match the airing
		this.airing = this.$store.state.your_airings[this.$route.params.INDEX];
		this.show_selected = this.airing.SID;
		this.theatre_selected = this.airing.TID;
		this.date = this.airing.DATE;
		this.strt_time = this.airing.STRT_TIME;
		this.stop_time = this.airing.STOP_TIME
		//console.log('airing:',this.airing,'show_selected:',this.show_selected,'this.theatre_selected:',this.theatre_selected, 'date:',this.date)

		// fetching theatres made by the current user
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
		
		//making a fetch to fill airings_date_tid at the start (before the damned watchers do)
		fetch('http://192.168.148.107:8000/get_airings_date_tid',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token,
					},
				body: JSON.stringify({'date':this.date, 'tid':this.theatre_selected})	})																				// this bracket is the end of fetch

				.then(response => response.json())

				.then(data => {
					for (var i in data)
						this.airings_date_tid.push(data[i]);
						//console.log(this.airings_date_tid)
					})																			//this bracket is the end of the then bloc

				.catch((error) => {
						console.error('Error: ', error)
					});	
	},

	methods: {

		submitform(event){
			fetch('http://192.168.148.107:8000/airings_post',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token,
					'action': this.action
					},
				body: JSON.stringify({'aid':this.airing.AID, 'show_selected':this.show_selected, 'theatre_selected':this.theatre_selected, 'date':this.date, 'strt_time':this.strt_time, 'stop_time':this.stop_time}),
				})																				// this bracket is the end of fetch

			.then(response => response.json())

			.then(data => {
				console.log(data.msg);
				router.push({name:'Your_airings'})
				})																				//this bracket is the end of the then block

			.catch((error) => {
					console.error('Error: ', error)
				});																				//these brackets are the end of the try blcok
		},

		date_format(value, event){
			return moment(value).format('YYYY-MM-DD')
		},

		time_format(value,event){
			return moment(value).format('h:mm')
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