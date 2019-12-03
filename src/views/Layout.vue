<template>
    <div class="layout">
        <Layout>
            <Header>
                <div class="layout-nav">
                    <Menu active-name="1-2" mode="horizontal" theme="dark" width="auto" :class="menuitemClasses">
                        <router-link to="/">
                        <MenuItem name="1-1">
                            <Icon type="ios-navigate"></Icon>
                            <span>系统首页</span>
                        </MenuItem>
                        </router-link>
                        <router-link to="/accountmanagement">
                        <MenuItem name="1-2">
                            <Icon type="ios-search"></Icon>
                            <span>账户管理</span>
                        </MenuItem>
                        </router-link>
                        <router-link to="/checkin">
                        <MenuItem name="1-3">
                            <Icon type="ios-settings"></Icon>
                            <span>一键签到</span>
                        </MenuItem>
                        </router-link>
                    </Menu>
                </div>
            </Header>
            <Content :style="{margin: '20px', background: '#fff', minHeight: '220px'}">
                <Card>
                    <slot></slot>
                </Card>  
            </Content>
            <Footer class="layout-footer-center">2019-2020 &copy; HduBroHelp</Footer>
        </Layout>
    </div>
</template>
<script>
    export default {
        data () {
            return {
                isCollapsed: false
            };
        },
        computed: {
            menuitemClasses: function () {
                return [
                    'menu-item',
                    this.isCollapsed ? 'collapsed-menu' : ''
                ]
            }
        }
    }
</script>
<style scoped>
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        position: relative;
        border-radius: 4px;
        overflow: hidden;
    }
    .layout-nav{
        position:relative;
        left: -14%;
        width: 150%;
        margin: auto;
    }
    .layout-footer-center{
        text-align: center;
    }
</style>