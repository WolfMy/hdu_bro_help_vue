<template>
<div>
    <h1 align="center">一键签到</h1>
    <Divider />
    <span>接口使用情况</span>
    <Progress :percent="IterfaceUsed" :stroke-color="['#87d068','#FF4500']" />
    <Table border ref="selection" :columns="columns" :data="data" @on-selection-change="updateSelection($event)"></Table>
    <br>
    <Input type="text" maxlength="4" v-model="checkCode" placeholder="请输入签到码..."/>
    <br><br>
    <Button type="primary" :loading="loading" @click="signin" long>
        <span v-if="!loading">一键签到</span>
        <span v-else>签到中...</span>
    </Button>
</div>
</template>
<script>
import Axios from 'axios';
const api_baseUrl = 'http://120.27.192.52:8080/';
//const api_baseUrl = 'http://127.0.0.1:5000/';
export default {
    data() {
        return {
            IterfaceUsed: 0,
            checkCode: '',
            loading: false,
            tokens: [],
            columns: [
                {
                    type: 'selection',
                    width: 60,
                    align: 'center'
                },
                {
                    title: '姓名',
                    key: 'name'
                },
                {
                    title: '学号',
                    key: 'studentnum'
                },
            ],
            data: []
        }
    },
    methods:{
        toLoading () {
            this.loading = true;
        },
        getIterfaceUsed() {
            var api = api_baseUrl + 'getIterfaceUsed'
            Axios.get(api).then((res)=>{
                this.IterfaceUsed = Number(res.data)
            })
        },
        getAccounts() {
            var api = api_baseUrl + 'getAccounts';
            Axios.get(api).then((res)=>{
                this.data = res.data;
                //console.log(res.data);
            }).catch((error)=>{
                console.log(error);
            })
        },
        updateSelection(event) {
            this.tokens = [];
            for(var key in event){
                var bro = event[key];
                this.tokens.push(bro.token);
            }
        },
        signin() {
            this.loading = true;
            var api = api_baseUrl + 'signin';
            var data = {'checkCode':this.checkCode, 'tokens':this.tokens}
            Axios.post(api, data).then((res)=>{
                this.loading = false;
                for(var key in res.data){
                    var state = res.data[key]
                    this.$Message[state['type']]({
                        background: true,
                        content: state['content'],
                        duration: 10,
                        closable: true
                    });
                    Axios.get(api_baseUrl + 'Iterface_Use');
                    this.getIterfaceUsed();
                }
            }).catch((error)=>{
                console.log(error);
            })
        }
    },
    mounted(){
        this.getAccounts();
        this.getIterfaceUsed();
    }
}
</script>