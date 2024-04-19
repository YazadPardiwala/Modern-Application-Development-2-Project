//PLS NOTE Venueops.vue is for testing. In actual usage this form would be linked to the tab or thing....actually I'm not sure how all this will come together but we'll figuire it out. Whether I'll figure it out in time...that's a seperate issue
//the app should at the time of creation fetch from the server all theatre names, & the venueops form should crosscheck these before letting you submmit (to ensure names are unique)
<template>
<div>
	<Maketheatre_form/>
</div>
</template>

<script>
	import Maketheatre_form from '@/components/Maketheatre_form.vue'

	export default{
		name: 'Venueops',
		components:{
			Maketheatre_form
		}
	}
</script>
	
<style scoped>
</style>
