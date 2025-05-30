import COS from 'cos-js-sdk-v5'

// 从环境变量获取密钥，避免硬编码敏感信息
export const cos = new COS({
    SecretId: import.meta.env.VITE_COS_SECRET_ID, // 使用环境变量存储身份识别ID
    SecretKey: import.meta.env.VITE_COS_SECRET_KEY // 使用环境变量存储身份秘钥
})


