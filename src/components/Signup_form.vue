<template>
<div>
	<h3>
		Pls do Signup, it would make us very happy.
	</h3>
	<form @submit.prevent="submitform">
		<div>
			<label for="name">Name:</label> <br>
			<input type="text" id="name" v-model='name'>
		</div>
		<div>
			<label for="email">Email:</label> <br>
			<input type="text" id="email" v-model='email'>
		</div>
		<div>
			<label for="password"> Password: </label> <br>
			<input type="password" id="password" v-model='password'>
		</div>
		<div>
			<label for="password_conf"> Confirm Password: </label> <br>
			<input type="password" id="password_conf" v-model='password_conf'>
		</div>
		<div>
			<button type="submit">Submit</button> 
		</div>
	</form>
</div>
</template>


<script>
	import store from '@/store/index.js'
	import router from '@/router/index.js'

	export default {
  name: 'Signup_form',
  data(){
		return{
			name: "",
			password: "",
			password_conf : "",
			email:""
		}
	},
	methods:{
		submitform(event){
			fetch('http://192.168.148.107:8000/sign_up',{
				method:'POST',
				headers: {
					'Content-Type':'application/json',
					},
				body: JSON.stringify({'name':this.name, 'password':this.password, 'password_conf':this.password_conf, 'email':this.email}),
				})																				// this bracket is the end of fetch
			.then(response => response.json())
			.then(data => {
				let payload = {'login_token' : data.token, 'user_curr' : data.user_curr, 'admin':data.admin}
				store.commit('login', payload);
				console.log(this.$store.state.token);
				console.log(this.$store.state.user_curr);
				console.log(this.$store.state.admin)
				router.push('/Future_shows')
				})																				//this bracket is the end of the then block
			.catch((error) => {
					console.error('Error: ', error)
				});																				//these brackets are the end of the try blcok

		}
	}
}
</script>

<style scoped>
	h3 {
		text-align: center;
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