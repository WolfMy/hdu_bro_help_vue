<template>
<div>
    <h1 align="center">数字杭电账户管理</h1>
    <Divider />
    <Row>
        <Col>
            <Form ref="formInline" inline>
                <FormItem required>
                    <Input type="text" v-model="studentnum" placeholder="Username">
                        <Icon type="ios-person-outline" slot="prepend"></Icon>
                    </Input>
                </FormItem>
                <FormItem required>
                    <Input type="password" v-model="password" placeholder="Password">
                        <Icon type="ios-lock-outline" slot="prepend"></Icon>
                    </Input>
                </FormItem>
                <FormItem>
                    <Button type="primary" @click="hdu_login()" :loading="loading">
                        <span v-if="!loading">登陆</span>
                        <span v-else>登陆中...</span>
                    </Button>
                </FormItem>
            </Form>
        </Col>
    </Row>
    <Row>
        <div style="padding: 10px;background: #f8f8f9">
            <Card title="Bros" icon="ios-contacts" :padding="0" shadow>
            <CellGroup>
                <Cell v-for="(bro, index) in data" :title="bro.name+' ('+bro.studentnum+')'" :label="bro.token" :key="bro.token">
                    <Icon v-if="!status[index]" type="ios-contact" size="20" slot="icon" />
                    <Icon v-if="status[index]" type="ios-alert-outline" color="red" size="20" slot="icon" />
                    <Icon type="ios-close-circle" size="16" slot="extra" @click="deleteAccount(index)" />
                    <!--Button slot="extra" type="error" size="small" @click="deleteAccount(index)">Delete</Button-->
                </Cell>
            </CellGroup>
            </Card>
        </div>
    </Row>
</div>
</template>

<script>
    import Axios from 'axios';
    export default {
        data () {
            return {
                studentnum: '',
                password: '',
                loading: false,
                data: [],
                status: [],
            }
        },
        methods: {
            getAccounts() {
                var api = this.$api_baseUrl + 'getAccounts'
                Axios.get(api).then((res)=>{
                    this.data = res.data;
                    //console.log(res.data);
                }).catch((error)=>{
                    console.log(error);
                })
            },
            checkTokenStatus() {
                var api = this.$api_baseUrl + 'checkTokenStatus'
                Axios.get(api).then((res)=>{
                    for(var index in res.data){
                        res.data[index] = !res.data[index]
                    }
                    this.status = res.data;
                    //console.log(res.data);
                }).catch((error)=>{
                    console.log(error);
                })
            },
            hdu_login() {
                this.loading = true;
                var api = this.$api_baseUrl + 'hdu_login'
                var data = {'studentnum':this.studentnum, 'password':this.password};
                Axios.post(api, data).then((res)=>{
                    console.log(res.data);
                    if(res.data == 'failed!'){
                        this.$Message.error('登陆失败，请重试！')
                    }else{
                        this.$Message.success('登陆成功')
                    }
                    this.loading = false;
                    this.studentnum = '';
                    this.password = '';
                    this.getAccounts();
                }).catch((error)=>{
                    console.log(error);
                })
                
            },
            deleteAccount(index) {
                var api = this.$api_baseUrl + 'deleteAccount'
                var data = {'studentnum':this.data[index].studentnum}
                Axios.post(api, data).then((res)=>{
                    console.log(res.data);
                    this.getAccounts();
                    this.$Message.success('删除成功')
                }).catch((error)=>{
                    console.log(error);
                })
            }
        },
        mounted() {
            this.getAccounts();
            this.checkTokenStatus();
        }
    }
</script>
