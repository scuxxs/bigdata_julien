<template>
  <table class="login-table" border="0" cellpadding="10">
    <tr>
      <td align="center">用户名</td>
      <td><input id='uid' type="text" v-model="uid" placeholder="请输入用户名"/></td>
    </tr>
    <tr>
      <td align="center">密&nbsp;&nbsp;&nbsp;&nbsp;码</td>
      <td><input id='password' type="password" v-model="password" placeholder="请输入密码"/></td>
    </tr>
    <tr align="center">
      <td colspan="2">
        <button @click="handleLogin">登录</button>
      </td>
    </tr>
  </table>
</template>

<script setup>
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import axios from "axios";
import {bool} from "mockjs/src/mock/random/basic.js";
const router = useRouter();
const uid = ref('');
const password = ref('');

async function handleLogin() {
  try {
    const response = await axios.post('/api/userManage/login', {uid: uid.value, password: password.value});
    console.log(response.data.code)
    if (response.data.code === 200) {
      const accessToken = response.headers['access_token'];
      console.log(accessToken)
      localStorage.setItem('accessToken', accessToken);
      const refreshToken = response.headers['refresh_token'];
      console.log(refreshToken)
      localStorage.setItem('refreshToken', refreshToken);
      if(response.data.data.authorization){
        router.replace('/home')
      }
      else {
        router.replace('/student')
      }
      // 使用后端返回的路径
    } else if (response.data.code === -1) {
      alert(response.data.msg);
      uid.value = '';
      password.value = '';
      document.getElementById('uid').focus();
    }
  } catch (error) {
    console.error("Error during login:", error.message); // 添加错误处理，打印错误信息
  }
}


</script>

<style lang="less" scoped>
/* 重置table样式 */
.login-table {
  width: 100%;
  max-width: 300px;
  margin: 50px auto;
  border-collapse: collapse;
  border-spacing: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.login-table td {
  padding-bottom: 16px;
  padding-top: 16px;
  padding-right: 0px;
  padding-right: 8px;
  vertical-align: middle;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.login-table input[type="text"],
.login-table input[type="password"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
  box-sizing: border-box;
}

.login-table button {
  display: block;
  width: 100%;
  padding: 12px;
  background-color: #007bff;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
  transition: all 0.3s ease;

  &:hover,
  &:focus {
    background-color: #0056b3;
  }
}
</style>
