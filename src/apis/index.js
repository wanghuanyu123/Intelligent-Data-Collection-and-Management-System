import request from '@/utils/request'
// 提交任务
export const submitApi = (data)=>{
    return request({
        url: '/submit',
        method: 'post',
        data,
    })
}

// //添加成员

// export const addroleApi = (data)=>{
//     return request({
//         url: '/addrole',
//         method: 'post',
//         data,
//     })
// }

// 获取成员列表
export const getroleListApi = ()=>{
    return request({
        url: '/getroleList',
        method: 'get',
    })
}

// 删除人员

export const deleteroleApi = (data)=>{
    return request({
        url: '/deleterole',
        method: 'post',
        data,
    })
}

// 获取新闻列表
export const getnewsListApi = ()=>{
    return request({
        url: '/newsList',
        method: 'get',
    })
}
/////////////////////////////////////////////////////////////////////////////////
// 注册
export const RegistApi = (data)=>{
    return request({
        url: '/regist',
        method: 'post',
        data,
    })
}

// 登录
export const LoginApi = (data)=>{
    return request({
        url: '/login',
        method: 'post',
        data,
    })
}

//添加人脸
export const addFaceApi = (data)=>{
    return request({
        url: '/addFace',
        method: 'post',
        data,
    })
}

//修改密码
export const changePasswordApi = (data)=>{
    return request({
        url: '/change_password',
        method: 'post',
        data,
    })
}

// 获取个人信息
export const getPersonInfoApi = (data)=>{
    return request({
        url: '/getPersonInfo',
        method: 'post',
        data,
    })
}

//提交老师
export const submitTeacherApi = (data)=>{
    return request({
        url: '/submitTeacher',
        method: 'post',
        data,
    })
}

// 获取审核任务
export const getTaskApi = (data)=>{
    return request({
        url: '/getTask',
        method: 'post',
        data
    })
}

// 学生获取发布记录
export const getStudentSaskApi =(data)=>{
    return request({
        url: '/getStudentSask',
        method: 'post',
        data
    })
}

//老师获取审核记录
export const getTeacherTask =(data)=>{
    return request({
        url: '/getTeacherTask',
        method: 'post',
        data
    })
}
// 老师通过
export const applyPassApi =(data)=>{
    return request({
        url: '/applyPass',
        method: 'post',
        data
    })
}
// 老师驳回
export const fallApi = (data)=>{
    return request({
        url: '/reject',
        method: 'post',
        data
    })
}

// 学生再次提交
export const addmoreApi = (data)=>{
    return request({
        url: '/addmore',
        method: 'post',
        data
    })
}
//添加俱乐部

export const addClubApi = (data)=>{
    return request({
        url: '/addclub',
        method: 'post',
        data
    })
}

// 获取俱乐部信息

export const getClubInfoApi = ()=>{
    return request({
        url: '/getclub',
        method: 'get',
    })
}

// 删除俱乐部
export const deleteClubApi = (data)=>{
    return request({
        url: '/deleteclub',
        method: 'post',
        data
    })
}

// 获取俱乐部信息
export const getClubInfoListApi = (data)=>{
    return request({
        url: '/clubInfo',
        method: 'post',
        data
    })

}
//添加俱乐部成员
export const addClubMenberApi = (data)=>{
    return request({
        url: '/addclubmenber',
        method: 'post',
        data
    })
}

//获取俱乐部成员
export const getClubMenberApi = (data)=>{
    return request({
        url: '/getclubmenber',
        method: 'post',
        data
    })
}

// 删除俱乐部成员
export const deleteMemberApi = (data)=>{
    return request({
        url: '/deleteclubmenber',
        method: 'post',
        data
    })

}

//查询俱乐部全部信息
export const lastStep = (data)=>{
    return request({
        url: '/showclubresult',
        method: 'post',
        data
    })
}

//#查看自己俱乐部
export const get_clubApi = (data)=>{
    return request({
        url: '/competition/club',
        method: 'post',
        data
    })
}

//添加班级
export const addClassApi = (data)=>{
    return request({
        url: '/addclass',
        method: 'post',
        data
    })
}

//获取班级列表
export const getClassListApi = ()=>{
    return request({
        url: '/getclass',
        method: 'get',
    })
}

// 删除班级
export const deleteClassApi = (data)=>{
    return request({
        url: '/deleteclass',
        method: 'post',
        data
    })
}

//获取班级列表
export const getStudentListApi = (data)=>{
    return request({
        url: '/getclasslist',
        method: 'post',
        data
    })
}

//添加班级成员
export const addClassMenberApi = (data)=>{
    return request({
        url: '/addclassmenber',
        method: 'post',
        data
    
    })
}

//获取班级成员信息
export const getclassMenberApi = (data)=>{
    return request({
        url: '/getclassmenber',
        method: 'post',
        data
    })
}

// 删除班级成员
export const deleteclassMemberApi = (data)=>{
    return request({
        url: '/deleteclassmenber',
        method: 'post',
        data
    })

}

//获取自己班级
export const getmyclassApi = (data)=>{
    return request({
        url: '/getmyclass',
        method: 'post',
        data
    })
}

//教师发布作业
export const addhomeworkApi = (data)=>{
    return request({
        url: '/teacherpublish',
        method: 'post',
        data
    })
}

//学生获取作业任务
export const gethomeworkApi = (data)=>{
    return request({
        url: '/studentgetwork',
        method: 'post',
        data
    })
}

//学生提交作业
export const submitworkApi = (data)=>{
    return request({
        url: '/submitworkApi',
        method: 'post',
        data
    })
}

//学生继续提交
export const continueworkApi = (data)=>{
    return request({
        url: '/continueSubmit',
        method: 'post',
        data
    })
}

//学生获取历史作业
export const gethistoryworkListApi = (data)=>{
    return request({
        url: '/gethistoryworklist',
        method: 'post',
        data
    })
}

//教师获取历史作业
export const gethistoryworkListTeacherApi = (data)=>{
    return request({
        url: '/Teachergethistoryworklist',
        method: 'post',
        data
    })
}

//教师获取某历史作业的学生提交内容
export const TeachergethistoryworkApi = (data)=>{
    return request({
        url: '/Teachergethistorywork',
        method: 'post',
        data
    })
}

//老师批改作业
export const TeachercheckworkApi = (data)=>{
    return request({
        url: '/grade_work',
        method: 'post',
        data
    })
}