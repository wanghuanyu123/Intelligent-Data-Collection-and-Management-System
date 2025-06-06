import axios from 'axios';
// 创建实例时配置默认值
const request = axios.create({
    baseURL: 'http://localhost:5000/api',
    timeout: 50000
  });

const loading = {}

// 添加请求拦截器
request.interceptors.request.use(function (config) {
    loading.value = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })
 
    // 在发送请求之前做些什么
    return config;
  }, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
  });

// 添加响应拦截器
request.interceptors.response.use(function (response) {
    // 2xx 范围内的状态码都会触发该函数。
    // 对响应数据做点什么
    const {data,message,success} = response.data
    
    // console.log(message,success);
    if(success){
      loading.value.close()
      return data
    }
    else{
      ElMessage({
        message: message,
        type: 'error',
      })
      loading.value.close()
      return Promise.reject(new Error(message || 'Error'))
    }
  }, function (error) {
    // 超出 2xx 范围的状态码都会触发该函
    // 对响应错误做点什么
    //过期访问
    loading.value.close()
    ElMessage({
      message: error.message,
      type: 'error',
    })
    return Promise.reject(error)
  });

export default request