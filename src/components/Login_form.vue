<template>
<div>
	<h3>
		Please do log in.
	</h3>
	<form @submit.prevent="submitform">
		<div>
			<label for="name">Name:</label> <br>
			<input type="text" id="name" v-model='name'>
		</div>
		<div>
			<label for="password"> Password: </label> <br>
			<input type="password" id="password" v-model='password'>
		</div>
		<div>
			<button type="submit">Submit</button> 
		</div>
	</form>
</div>
</template>

<script>
	import router from '@/router/index.js'
	import store from '@/store/index.js'

	export default {
  name: 'Login_form',

  data(){
		return{
			name: "",
			password: "",
		}
	},

	methods:{
		submitform(event){
			fetch('http://192.168.148.107:8000/',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					},
				body: JSON.stringify({'name':this.name, 'password':this.password}),
				})																				// this bracket is the end of fetch

			.then(response => response.json() )

			.then(data => {
				//console.log(data.token)
				let payload = {'login_token' : data.token, 'user_curr' : data.user_curr, 'admin':data.admin}
				store.commit('login', payload);
				console.log(this.$store.state.token);
				console.log(this.$store.state.user_curr);
				console.log(this.$store.state.admin)
				router.push('/Future_shows')
				})																				//this bracket is the end of the then block

			.catch((error) => {
					console.log(error)
					
				});																				//these brackets are the end of the try blcok

		},
	}
}
</script>

<style scoped>
	h3 {
		text-align: center;
		margin-right: 400px
	}

	input {
		margin-top: 7px;
	}
	div{
		margin: 15px
	}

	button{
		margin: 10px
	}
</style>