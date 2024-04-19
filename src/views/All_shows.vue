//THIS PAGE IS NOT FIT FOR FINAL USE YET. PLS BE ADVISED.

<template>
<div>

	<div>
	<form @submit.prevent="submitform">
		<h3>
			<label for="search_val"> Are there any particular shows you want: </label> <br>
			<input type="text" id="search_val" v-model="search_val">
			<button type="submit">Search?</button> 
		</h3>
	</form>
	</div>

	<div v-if="search == false">
		You are now looking at the page with all Shows 
		<table class = "table">
			<thead>
				<tr>
					<th scope = "col"> # </th>
					<th scope = "col">Show Name </th>
					<th scope = "col"> Description </th>
					<th scope = "col"> Price</th>
					<th scope = "col"> Rating</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="(show, index) in all_shows">
					<td> {{index+1}} </td>
					<td> {{show.SNAME}} </td>
					<td> <textarea> {{show.S_DESCR}} </textarea> </td>
					<td> {{show.PRICE}} </td>
					<td> {{show.RATING_AGG}} </td>
					<td> <button v-on:click="redirect_rate(`${index}`,'all_shows')" > &emsp; Rate &emsp; </button> </td>
				</tr>
				<br>
			</tbody>
		</table>
	</div>

	<div v-if="search == true">
		Here is the show you looked for
		<div>
			<table class = "table">
			<thead>
				<tr>
					<th scope = "col"> # </th>
					<th scope = "col">Show Name </th>
					<th scope = "col"> Description </th>
					<th scope = "col"> Price</th>
					<th scope = "col"> Rating</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="(show, index) in specific_shows">
					<td> {{index+1}} </td>
					<td> {{show.SNAME}} </td>
					<td> {{show.S_DESCR}} </td>
					<td> {{show.PRICE}} </td>
					<td> {{show.RATING_AGG}} </td>
					<td> <button v-on:click="redirect_rate(`${index}`,'specific_shows')" > &emsp; Rate &emsp; </button> </td>
				</tr>
				<br>
			</tbody>
		</table>
		</div>
		<div>
			<button @click="revert"> Go back to the list of all shows? </button>
		</div>
	</div>
</div>
</template>



<script>
import store from '@/store/index.js'
import router from '@/router/index.js'

export default{
	name: 'All_shows',
	data(){
		return{
			all_shows: [],
			specific_shows: [],
			search_val:'',
			search:false
		}
	},

	beforeMount(){

		this.specific_shows = this.$store.state.specific_shows
		this.search = this.$store.state.show_searched
		//console.log(this.specific_shows)

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
	},

	methods:{

		submitform(event){
				this.search=true
				console.log(this.search)

				fetch('http://192.168.148.107:8000/specific_shows_get',{
					method:'POST',
					headers: {
						'Content-Type':'application/json',
						'login-token':this.$store.state.token,
						},
					body: JSON.stringify({'search_val':this.search_val}),
					})																				// this bracket is the end of fetch

				.then(response => response.json())

				.then(data => {
					this.specific_shows=[];
					for (var i in data)
						this.specific_shows.push(data[i]);

					let payload = {'specific_shows' : this.specific_shows}
					store.commit('add_specific_shows', payload)
					//console.log(this.$store.state.specific_shows)

					})																			//this bracket is the end of the then bloc
				.catch((error) => {
						console.error('Error: ', error)
					});																				//these brackets are the end of the try blcok
			},
	
		revert(event){
				this.search=false
				store.commit('remove_specific_shows')
			},

		redirect_rate(Index, Show_list){
				router.push({name:'Rateshow_form', params: {show_list: `${Show_list}`, index: `${Index}`}})
			},

	}

}
</script>

<style scoped>
textarea{
	cols: 150;
	rows: 3
}
</style>