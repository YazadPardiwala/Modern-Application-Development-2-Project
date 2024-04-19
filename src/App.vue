<template>
  <nav>
    <router-link :to="{name: 'Login_pg'}"> Login | </router-link> 
    <router-link :to="{name: 'Signup_pg'}"> Sign up | </router-link> 
    <router-link :to="{name: 'Future_shows'}"> Shows airing soon | </router-link>  
    <router-link :to="{name: 'All_shows'}"> All shows | </router-link>
    <router-link :to="{name: 'All_theatres'}"> Theatres | </router-link>
    <router-link :to="{name: 'Maketheatre_form'}" v-if="this.$store.state.admin===1"> Create Venue | </router-link> 
    <router-link :to="{name: 'Your_theatres'}" v-if="this.$store.state.admin===1"> Your Theatres | </router-link>
    <router-link :to="{name: 'Makeshow_form'}" v-if="this.$store.state.admin===1"> Create a Show | </router-link>
    <router-link :to="{name: 'Your_shows'}" v-if="this.$store.state.admin===1"> Your Shows | </router-link>
    <router-link :to="{name: 'Makeairing_form'}" v-if="this.$store.state.admin===1"> Create a Show airing | </router-link>
    <router-link :to="{name: 'Your_airings'}" v-if="this.$store.state.admin===1"> Your airings | </router-link>
    <router-link :to="{name: 'Booked_shows'}"> Your Bookings </router-link>  
  </nav>
  <router-view/>
</template>

<script>
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

h3{
    text-align: left;
    margin-left: 50px
}
table{
    border: 2px solid;
    margin-left: auto;
    margin-right: auto
}
tr, th, td{
    border: 1px solid;
    padding:5px
}
thead{
    margin-top:20 px;
    margin-bottom: 20px
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>

