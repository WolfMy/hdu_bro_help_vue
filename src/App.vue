<template>
<div id="app">
    <layout>
        <router-view></router-view>
    </layout>
</div>
</template>

<script>
import Layout from './views/Layout.vue'

export default {
    components:{
        'layout': Layout,

    }
}
</script>