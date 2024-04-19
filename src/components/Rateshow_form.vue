<template>
<div>
	<h3>
	How did you find the show {{show.SNAME}}
	</h3>
	<form @submit.prevent="submitform">

		<p>
			<table>
			<thead> </thead>
				<tbody>
					<tr>
						<td> <label for ="1"> Hot Garbage (1/5) </label> </td>
						<td> <input type = "radio" id="1" v-model="rating" value="1"></td> 
					</tr>
					<tr>
						<td> <label for ="2"> It had some redeeming qualities (2/5) </label> </td>
						<td> <input type = "radio" id="2" v-model="rating" value="2"> </td>
						
					</tr>
					<tr>
						<td> <label for = "3"> Decent (3/5) </label> </td>
						<td> <input type = "radio" id="3" v-model="rating" value="3"> </td> 
						
					</tr>
					<tr>
						<td> <label for = "4"> Pretty Good (4/5) </label>  </td>
						<td> <input type = "radio" id="4" v-model="rating" value="4"> </td>
					</tr>
					<tr>
						<td> <label for = "5"> Extremely Good/Perfect (5/5) </label> </td>
						<td> <input type = "radio" id="5" v-model="rating" value="5"> </td>
					</tr>
				</tbody>
			</table>
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
	name:'Rateshow_form',

	data(){
		return{
			index:'',
			show_list:'',
			show:{},
			rating:''
		}
	},

	beforeMount(){
		this.index = this.$route.params.index;
		this.show_list = this.$route.params.show_list;

		if(this.show_list === 'all_shows'){
			this.show = this.$store.state.all_shows[this.index]
		};

		if(this.show_list === 'specific_shows'){
			this.show = this.$store.state.specific_shows[this.index]
		};	
		


	},

	methods: {
		submitform(event){
			fetch('http://192.168.148.107:8000/ratings_post',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					'login-token':this.$store.state.token
					},
				body: JSON.stringify({'SID': this.show.SID , 'rating':this.rating}),
				})																				// this bracket is the end of fetch

			.then(response => response.json())

			.then(data => {
				//console.log(data.msg);
				router.push({name:'All_shows'})
				})																				//this bracket is the end of the then block

			.catch((error) => {
					console.error('Error: ', error)
				});		
		},
	}


}

</script>

<style scoped>

</style>