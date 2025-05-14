from flask import Flask, render_template, request,jsonify
from flask_cors import CORS
from app import driver
import random
from tencent_cloud_sample.sample import addRole ,deleterole
from submitFun import submitFun,submitPhotos,submitFile
from createToken import createToken
import json
app = Flask(__name__)
CORS(app)

# 注册
@app.route('/api/regist', methods=['Post'])  
def resgister():
    data = request.get_json()
    PersonName = data.get('PersonName')
    PersonId = data.get('PersonId')
    PersonRole = data.get('PersonRole')  # 这里应该是 PersonRole 而不是 GePersonRolender
    password = data.get('password')
    # print(PersonName,PersonId,PersonRole,password)
    # 检查PersonId是否已经存在
    with driver.session() as session:
        result = session.run("MATCH (p:Person) WHERE p.PersonId = $id RETURN p", id=PersonId)
        
        if result.single():
            # 如果PersonId已存在，可以在这里添加登录逻辑
            return jsonify({"status": 200, "success":False,"message": "该角色已存在"}), 200
        else:
            # 如果PersonId不存在，创建新的Person节点
            session.run("CREATE (p:Person {PersonId: $id, PersonName: $name, PersonRole: $role,password:$password})",
                        id=PersonId, name=PersonName, role=PersonRole, password=password)
            return jsonify({"status": 200, "success":True,"message": "创建成功"}), 201

#登录
@app.route('/api/login', methods=['Post'])
def login():
    data = request.get_json()
    PersonName = data.get('PersonName')
    PersonId = data.get('PersonId')
    password = data.get('password')
    # print(PersonName, PersonId, password)

    with driver.session() as session:
        # 执行查询，包括PersonRole属性
        result = session.run(
            "MATCH (p:Person) "
            "WHERE p.PersonId = $PersonId "
            "AND p.password = $password "
            "AND p.PersonName = $name "
            "RETURN p { .PersonRole } AS personRole",
            {"PersonId": PersonId, "password": password, "name": PersonName}
        )
        
        # 检查是否有匹配的节点
        single_record = result.single()
        if single_record:
            # 登录成功，创建token，并提取PersonRole属性
            token = createToken(PersonName)
            personRole = single_record["personRole"]
            return jsonify({
                "status": 200,
                "success": True,
                "message": "登录成功",
                'data': {
                    'token': token,
                    'PersonRole': personRole  # 添加PersonRole属性
                }
            }), 200
        else:
            # 登录失败
            return jsonify({
                "status": 200,
                "success": False,
                "message": "登录失败"
            }), 200

# 录入人脸
@app.route('/api/addFace', methods=['Post'])  
def addPersonaddFace():
    data = request.get_json()
    # 从请求中获取所有需要的属性
    PersonId = data.get('PersonId')
    PhotoId = data.get('PhotoId')
    link = data.get('link')
    description = data.get('description')
    type = data.get('type')
    flag = False  # 假设请求中包含一个标记是否为主要照片的flag
    # print(PersonId, PhotoId, link, description, type, flag)
    # 检查必要的属性是否提供
    # if not all([PersonId, PhotoId, link, description, type, flag]):
    #     return jsonify({"status": 200, "success": False, "message": "缺少必要的字段"}), 200

    with driver.session() as session:
        # 根据PersonId匹配Person节点
        result = session.run(
            "MATCH (p:Person) "
            "WHERE p.PersonId = $PersonId "
            "RETURN p{ .PersonName } AS PersonName",
            {"PersonId": PersonId}
        )
        person_record = result.single()

        if not person_record:
            return jsonify({"status": 200, "success": False, "message": "该人员不存在"}), 200
        PersonName = person_record["PersonName"]
        # print(PersonName)
        if(addRole(PersonName['PersonName'],PersonId,link)):
            # 创建Photo节点和Person--hasPhoto-->Photo关系
            photo_node = {
                "id": PhotoId,
                "link": link,
                "description": description,
                "type": type,
                "time": session.run("RETURN timestamp()").single()[0]  # 获取当前时间戳
            }
            session.run(
                "MATCH (p:Person) "
                "WHERE p.PersonId = $PersonId "
                "CREATE (ph:Photo {id: $PhotoId, link: $link, description: $description, type: $type, time: $time}) "
                "CREATE (p)-[:hasPhoto {flag: $flag}]->(ph)",
                {
                    "PersonId": PersonId,
                    "PhotoId": PhotoId,
                    "link": link,
                    "description": description,
                    "type": type,
                    "time": photo_node["time"],
                    "flag": flag
                }
            )
            return jsonify({"status": 200, "success": True, "message": "入录人脸成功"}), 201
        else: return jsonify({"status": 401, "success": False, "message": "入录人脸失败"}), 401

#修改密码
@app.route('/api/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    PersonId = data.get('PersonId')
    new_password = data.get('newpass')

    with driver.session() as session:
        query = (
            "MATCH (p:Person {PersonId: $PersonId}) "
            "SET p.password = $new_password "
            "RETURN p"
        )
        result = session.run(query, {
            "PersonId": PersonId,
            "new_password": new_password
        })

        # 检查是否成功更新
        if result.single():
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Password changed successfully"
            }), 200
        else:
            return jsonify({
                "status": 404,
                "success": False,
                "message": "Person not found"
            }), 404


# 获取个人信息
@app.route('/api/getPersonInfo', methods=['Post'])       
def getPersonInfo():
    data = request.get_json()
    # 从请求中获取所有需要的属性
    PersonId = data.get('PersonId')

    if not PersonId:
        return jsonify({"status": 200, "success": False, "message": "缺少必要的字段"}), 400

    with driver.session() as session:
        # 查询Person节点和类型为“normal”的Photo节点
        result = session.run(
            "MATCH (p:Person)-[r:hasPhoto]->(ph:Photo) "
            "WHERE p.PersonId = $PersonId AND ph.type = 'normal' "
            "RETURN p, collect(ph) AS photos",
            {"PersonId": PersonId}
        )
        
        person_info = None
        photos = []
        for record in result:
            person = record["p"]
            photo_list = record["photos"]
            person_info = {
                "PersonId": person["PersonId"],
                "PersonName": person['PersonName'],
                "PersonRole": person['PersonRole'],
                "password":person['password']
            }
            for photo in photo_list:
                photos.append({
                    "PhotoId": photo["id"],
                    "link": photo["link"],
                    "description": photo["description"],
                    "type": photo["type"],
                    "time": photo["time"]
                })

        return jsonify({
            "status": 200,
            "success": True,
            "message": "获取个人信息成功",
            "data": {
                "person": person_info,
                "photos": photos
            }
        }), 200


# 提交任务
@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.get_json()
    photos = data.get('photos')
    # 人脸识别逻辑
    people_list = []
    datas = []
    datas,people_list = submitPhotos(photos)
    # print(datas,people_list)
    # 
    return jsonify({
                'status': 200,
                'success': True,
                'message': '任务提交成功',
                'data': {"dataList": datas,
                         "people_list": people_list
                         }
    }) 
# 学生提交作品给老师
@app.route('/api/submitTeacher', methods=['POST'])
def submitTeacher():
    data = request.get_json()
    Competition = data.get('Competition')
    CompetitionAchievement = data.get('CompetitionAchievement')
    peopleInfoList = data.get('peopleInfoList')
    PersonId = data.get('PersonId')
    photo = data.get('photo')
    docunment = data.get('fileList')
    paper = data.get('paper')
    achedoc = data.get('achedoc')
    clubName = data.get('ClubName')
    print(docunment, paper, achedoc)
    
    with driver.session() as session:
        # 查询PersonRole为“teacher”的Person节点
        person_ids = [info['PersonId'] for info in peopleInfoList if info.get('PersonRole') == 'teacher']
        if not person_ids:
            personname = [info['PersonName'] for info in peopleInfoList if info.get('PersonRole') == 'teacher']
            # 创建submitHistory节点，使用当前时间戳作为唯一标识
            submit_history_data = {
                'Competition': str(Competition),
                'CompetitionAchievement': str(CompetitionAchievement),  # 将复杂对象转换为字符串
                'peopleInfoList':str(peopleInfoList),  # 将复杂对象转换为字符串
                'created_at': session.run("RETURN timestamp()").single()[0],  # 使用创建时间作为唯一标识
                'status':0 , # 待定
                'photo':photo,
                'docunment':docunment,
                'paper':paper,
                'achedoc':achedoc,
                'clubName':clubName,
            }

            # 创建submitHistory节点
            create_submit_history = (
                "CREATE (sh:submitHistory $data) "
                "RETURN ID(sh)"
            )
            submit_history_id = session.run(create_submit_history, data=submit_history_data).single()[0]

            # 为每个教师节点和submitHistory节点建立关系
            for name in personname:
                print(name)
                session.run(
                    "MATCH (sh:submitHistory), (t:Person) "
                    "WHERE ID(sh) = $submitHistoryId AND t.PersonName = $PersonName) "
                    "CREATE (sh)-[:审核记录]->(t)",
                    submitHistoryId=submit_history_id,
                    PersonName=name,
                )

            return jsonify({
                "status": 200,
                "success": True,
                "message": "提交历史记录成功创建",
            }), 200
        # 创建submitHistory节点，使用当前时间戳作为唯一标识
        submit_history_data = {
            'Competition': str(Competition),
            'CompetitionAchievement': str(CompetitionAchievement),  # 将复杂对象转换为字符串
            'peopleInfoList':str(peopleInfoList),  # 将复杂对象转换为字符串
            'created_at': session.run("RETURN timestamp()").single()[0],  # 使用创建时间作为唯一标识
            'PersonId':PersonId,
            'photo':photo,
            'docunment':docunment,
            'paper':paper,
            'achedoc':achedoc,
            'status':0 , # 待定
            'clubName':clubName,
        }

        # 创建submitHistory节点
        create_submit_history = (
            "CREATE (sh:submitHistory $data) "
            "RETURN ID(sh)"
        )
        submit_history_id = session.run(create_submit_history, data=submit_history_data).single()[0]
        
        # 为每个教师节点和submitHistory节点建立关系
        for person_id in person_ids:
            session.run(
                "MATCH (sh:submitHistory), (t:Person) "
                "WHERE ID(sh) = $submitHistoryId AND t.PersonId = $personId  "
                "CREATE (sh)-[:审核记录]->(t)",
                submitHistoryId=submit_history_id,
                personId=person_id,
            )
        
        return jsonify({
            "status": 200,
            "success": True,
            "message": "提交历史记录成功创建",
        }), 200
# 老师获取指定提交的任务
@app.route('/api/getTask', methods=['Post'])
def getTask():
    data = request.get_json()
    PersonId = data.get('PersonId')
    if not PersonId:
        return jsonify({"status": 400, "success": False, "message": "PersonId is required"}), 400

    with driver.session() as session:
        # 查询Person节点下的审核记录关系下的submitHistory节点
        query = (
            "MATCH (sh:submitHistory)-[r:审核记录]->(p:Person) "
            "WHERE p.PersonId = $PersonId "
            "RETURN sh"
        )
        result = session.run(query, PersonId=PersonId)
        # print(result)
        tasks = []
        for record in result:
            # print(record)
            sh = record['sh']
            task_data = {key: value for key, value in sh.items()}
            # print(task_data)
            tasks.append(task_data)

        
        return jsonify({
            "status": 200,
            "success": True,
            "message": "Tasks retrieved successfully",
            "data": {
                "data": tasks
            }
        }), 200
# 学生获取自己提交的任务
@app.route('/api/getStudentSask', methods=['POST'])
def getStudentSask():
    data = request.get_json()
    PersonId = data.get('PersonId')
    if not PersonId:
        return jsonify({"status": 400, "success": False, "message": "PersonId is required"}), 400

    with driver.session() as session:
        # 查询Person节点下的审核记录关系下的submitHistory节点
        query = (
            "MATCH (sh:submitHistory) "
            "WHERE sh.PersonId = $PersonId "
            "RETURN sh"
        )
        result = session.run(query, PersonId=PersonId)
        # print(result)
        tasks = []
        for record in result:
            # print(record)
            sh = record['sh']
            task_data = {key: value for key, value in sh.items()}
            # print(task_data)
            tasks.append(task_data)

        
        return jsonify({
            "status": 200,
            "success": True,
            "message": "Tasks retrieved successfully",
            "data": {
                "data": tasks
            }
        }), 200

#获取老师审核记录
@app.route('/api/getTeacherTask', methods=['POST'])
def getTeacherTask():
    data = request.get_json()
    PersonId = data.get('PersonId')
    if not PersonId:
        return jsonify({"status": 400, "success": False, "message": "PersonId is required"}), 400

    with driver.session() as session:   
        query = (
            "MATCH (sh:submitHistory)-[r:审核记录]->(p:Person) "
            "WHERE p.PersonId = $PersonId "
            "RETURN sh"
        )
        result = session.run(query, PersonId=PersonId)
        # print(result)
        tasks = []
        for record in result:
            # print(record)
            sh = record['sh']
            task_data = {key: value for key, value in sh.items()}
            # print(task_data)
            tasks.append(task_data)


        return jsonify({
            "status": 200,
            "success": True,
            "message": "Tasks retrieved successfully",
            "data": {
                "data": tasks
            }
        }), 200
# 教师申请通过
@app.route('/api/applyPass', methods=['POST'])
def applyPass():
    data = request.get_json()
    created_at = data.get('created_at')
    if not created_at:
        return jsonify({"status": 400, "success": False, "message": "created_at is required"}), 400

    try:
        with driver.session() as session:
            # 找到created_at匹配的submitHistory节点并更新status属性
            query = (
                "MATCH (sh:submitHistory) "
                "WHERE sh.created_at = $created_at "
                "SET sh.status = 2 "
                "RETURN sh"
            )
            result = session.run(query, created_at=created_at)
            
            # 检查更新结果
            updated_nodes = []
            for record in result:
                updated_nodes.append(dict(record['sh'].items()))


                sh = record['sh']

                competition_json_str = sh['Competition']
                competition_achievement_json_str = sh['CompetitionAchievement']
                clubName = sh['clubName']
               

                # 将单引号替换为双引号
                competition_json_str = competition_json_str.replace("'", '"')
                competition_achievement_json_str = competition_achievement_json_str.replace("'", '"')
                
                # 解析JSON字符串
                competition_json = json.loads(competition_json_str)
                competition_achievement_json = json.loads(competition_achievement_json_str)
                
                # 获取当前时间戳
                current_timestamp = session.run("RETURN timestamp()").single()[0]
                
                # 添加created_at属性
                competition_json['id'] = current_timestamp

                # 添加俱乐部名称。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
                competition_json['clubName'] = clubName   
                #。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
                competition_achievement_json['id'] = current_timestamp
                
                # 使用解析后的数据创建新节点
                create_competition_query = (
                    "CREATE (:Competition $data)")
                create_competition_achievement_query = (
                    "CREATE (:CompetitionAchievement $data)")

                # # 执行创建操作
                session.run(create_competition_query, data=competition_json)
                session.run(create_competition_achievement_query, data=competition_achievement_json)
                competition_id = competition_json.get('id')
                competition_achievement_id = competition_achievement_json.get('id')
                
                peopleList_str = sh['peopleInfoList']
                peopleList_str = peopleList_str.replace("'", '"')
                peopleList = json.loads(peopleList_str)

                paperList = sh['paper']
                competition_description = competition_json.get('description', '')
                for index, paper in enumerate(paperList, start=1):
                    title = f"{competition_description}论文_{index}"
                    document_id = session.run("RETURN timestamp()").single()[0]  # 为Document节点创建唯一标识符
                    document_data = {
                        "id": document_id,
                        "title": title,
                        "type": "report",
                        "link": paper
                    }
                    create_document_query = (
                        "CREATE (:Document $data)")
                    session.run(create_document_query, data=document_data)

                    session.run(
                        "MATCH (c:Competition {id: $competition_id}), (d:Document {id: $document_id}) "
                        "CREATE (c)-[:HAS_ACHIEVEMENT {type: 1}]->(d)",
                        {"competition_id": competition_id, "document_id": document_id}
                    )

                    
                    for ranking, person_info in enumerate(peopleList, start=1):
                        session.run(
                            "MATCH (d:Document {id: $document_id}), (p:Person {PersonId: $person_id}) "
                            "MERGE (d)-[:BELONG {ranking: $ranking}]->(p)",
                            {"document_id": document_id, "person_id": person_info.get('PersonId'), "ranking": ranking}
                        )

                docunmentList = sh['docunment']
                for index, paper in enumerate(docunmentList, start=1):
                    title = f"{competition_description}文档_{index}"
                    document_id = session.run("RETURN timestamp()").single()[0]  # 为Document节点创建唯一标识符
                    document_data = {
                        "id": document_id,
                        "title": title,
                        "type": "document",
                        "link": paper
                    }
                    create_document_query = (
                        "CREATE (:Document $data)")
                    session.run(create_document_query, data=document_data)

                    session.run(
                        "MATCH (c:Competition {id: $competition_id}), (d:Document {id: $document_id}) "
                        "CREATE (c)-[:HAS_ACHIEVEMENT {type: 2}]->(d)",
                        {"competition_id": competition_id, "document_id": document_id}
                    )

                achedocList = sh['achedoc']
                for index, paper in enumerate(achedocList, start=1):
                    title = f"{competition_description}竞赛成果文档_{index}"
                    document_id = session.run("RETURN timestamp()").single()[0]  # 为Document节点创建唯一标识符
                    document_data = {
                        "id": document_id,
                        "title": title,
                        "type": "news",
                        "link": paper
                    }
                    create_document_query = (
                        "CREATE (:Document $data)")
                    session.run(create_document_query, data=document_data)

                    session.run(
                        "MATCH (c:CompetitionAchievement {id: $competition_achievement_id}), (d:Document {id: $document_id}) "
                        "CREATE (c)-[:EVIDENCE ]->(d)",
                        {"competition_achievement_id": competition_achievement_id, "document_id": document_id}
                    )

                print(peopleList)
                competition_achievement_id = competition_achievement_json.get('id')
                for person_info in peopleList:
                    person_id = person_info.get('PersonId')
                    person_role = person_info.get('PersonRole')
                    # print(person_id)
                    if person_id:
                        # 假设Competition节点有一个id属性
                        competition_id = competition_json.get('id')
                        session.run(
                            "MATCH (p:Person {PersonId: $person_id}), (c:Competition {id: $competition_id}) "
                            "CREATE (p)-[:PARTICIPATED_IN]->(c)",
                            person_id=person_id,
                            competition_id=competition_id
                        )

                        session.run(
                            "MATCH (ca:CompetitionAchievement {id: $competition_achievement_id}), (p:Person {PersonId: $person_id}) "
                            "MERGE (ca)-[:BELONG {type: $person_role}]->(p)",
                            competition_achievement_id=competition_achievement_id,
                            person_id=person_id,
                            person_role=person_role
                        )

                # 创建Competition到CompetitionAchievement的关系
                competition_achievement_id = competition_achievement_json.get('id')
                session.run(
                    "MATCH (c:Competition {id: $competition_id}), (ca:CompetitionAchievement {id: $competition_achievement_id}) "
                    "MERGE (c)-[:HAS_ACHIEVEMENT {type: 0}]->(ca)",
                    competition_id=competition_id,
                    competition_achievement_id=competition_achievement_id
                )

              
                photo_list = sh.get('photo', [])
                competition_id = competition_json['id']  # 确保这里有一个有效的competition_id

               
                for photo in photo_list:
                    photo_id = f"{competition_id}{photo}"
                    photo_data = {
                        "id": photo_id,
                        "link": photo,
                        "descript": "活动照片",
                        "time": session.run("RETURN timestamp()").single()[0],
                        "type": "licence"
                    }
                    create_photo_query = (
                        "CREATE (:Photo $data)")
                    photo_node = session.run(create_photo_query, data=photo_data).single()

                    # 创建Competition-[:HAS]->Photo关系
                    create_relation_query = (
                        "MATCH (c:Competition {id: $competition_id}), (p:Photo {id: $photo_id}) "
                        "CREATE (c)-[:HAS]->(p)")
                    session.run(create_relation_query, competition_id=competition_id, photo_id=photo_id)

                    session.run(
                        "MATCH (ca:CompetitionAchievement {id: $competition_achievement_id}), (p:Photo {id: $photo_id}) "
                        "CREATE (ca)-[:EVIDENCE]->(p)",
                        competition_achievement_id=competition_achievement_id,
                        photo_id=photo_id
                    )
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Status updated successfully",
                "data": updated_nodes
            }), 200
        

    except Exception as e:
        # 打印异常信息，用于调试
        print(str(e))
        # 返回500错误，表示服务器内部错误
        return jsonify({"status": 500, "success": False, "message": "An error occurred"}), 500
# 教师申请驳回
@app.route('/api/reject', methods=['POST'])
def reject():
    data = request.get_json()
    created_at = data.get('created_at')
    print(created_at)
    if not created_at:
        return jsonify({"status": 400, "success": False, "message": "created_at is required"}), 400

    try:
        with driver.session() as session:
            # 找到created_at匹配的submitHistory节点并更新status属性
            query = (
                "MATCH (sh:submitHistory) "
                "WHERE sh.created_at = $created_at "
                "SET sh.status = 1 "
                "RETURN sh"
            )
            result = session.run(query, created_at=created_at)
            updated_nodes = []
            for record in result:
                updated_nodes.append(dict(record['sh'].items()))
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Status updated successfully",
                "data": updated_nodes
            }), 200
    except Exception as e:
        # 打印异常信息，用于调试
        print(str(e))
        # 返回500错误，表示服务器内部错误
        return jsonify({"status": 500, "success": False, "message": "An error occurred"}), 500

# 学生再次提交
@app.route('/api/addmore', methods=['POST'])
def rejects():
    data = request.get_json()
    created_at = data.get('created_at')
    Competition = data.get('Competition')
    CompetitionAchievement = data.get('CompetitionAchievement')
    peopleInfoList = data.get('peopleInfoList')
    
    Competition = str(Competition)
    CompetitionAchievement = str(CompetitionAchievement)
    peopleInfoList = str(peopleInfoList)
    print(Competition)
    
    
    if not created_at:
        return jsonify({"status": 400, "success": False, "message": "created_at is required"}), 400

    try:
        with driver.session() as session:
            # 找到created_at匹配的submitHistory节点并更新status属性
            query = (
                "MATCH (sh:submitHistory) "
                "WHERE sh.created_at = $created_at "
                "SET sh.status = 0 "
                "SET sh.Competition = $Competition "
                "SET sh.CompetitionAchievement = $CompetitionAchievement "
                "SET sh.peopleInfoList = $peopleInfoList "
                "RETURN sh"
            )
            result = session.run(query, created_at=created_at,Competition=Competition,CompetitionAchievement=CompetitionAchievement,peopleInfoList=peopleInfoList)
            updated_nodes = []
            for record in result:
                updated_nodes.append(dict(record['sh'].items()))
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Status updated successfully",
                "data": updated_nodes
            }), 200
    except Exception as e:
        # 打印异常信息，用于调试
        print(str(e))
        # 返回500错误，表示服务器内部错误
        return jsonify({"status": 500, "success": False, "message": "An error occurred"}), 500

#添加俱乐部
@app.route('/api/addclub', methods=['POST'])
def addclub():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    teacher = data.get('teacher')
    if not name or not description or not teacher:
        return jsonify({"status": 400, "success": False, "message": "name, description, and teacher are required"}), 400

    try:
        with driver.session() as session:
            # 创建club节点
            query_create_club = (
                "CREATE (c:Club {name: $name, description: $description, teacher: $teacher}) "
                "RETURN c"
            )
            result = session.run(query_create_club, name=name, description=description, teacher=teacher)
            club_node = dict(result.single()['c'].items())

            # 获取club节点的ID
            club_id = club_node['name']

            # 创建club-[HAS]-->person的关系
            query_create_relationship = (
                "MATCH (c:Club), (p:Person {PersonId: $teacher}) "
                "WHERE c.name = $clubId "
                "CREATE (c)-[:HAS {role:$role}]->(p)"
            )
            session.run(query_create_relationship, clubId=club_id, teacher=teacher,role="teacher")

        return jsonify({"status": 200, "success": True, "message": "Club created successfully", "data": club_node}), 200

    except Exception as e:
        # 打印异常信息，用于调试
        print(str(e))
        # 返回500错误，表示服务器内部错误
        return jsonify({"status": 500, "success": False, "message": "An error occurred"}), 500

#获取俱乐部信息
@app.route('/api/getclub', methods=['GET'])
def getclub():
    try:
        with driver.session() as session:
            # 查询所有的club节点
            query = "MATCH (c:Club) RETURN c"
            result = session.run(query)

            # 准备一个列表来存储查询结果
            clubs = []
            for record in result:
                club_node = dict(record['c'].items())
                clubs.append(club_node)

            # 返回包含所有Club节点的JSON数组
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Clubs retrieved successfully",
                "data": clubs
            }), 200

    except Exception as e:
        # 打印异常信息，用于调试
        print(str(e))
        # 返回500错误，表示服务器内部错误
        return jsonify({"status": 500, "success": False, "message": "An error occurred"}), 500

#删除俱乐部
@app.route('/api/deleteclub', methods=['POST'])
def deleteclub():
    data = request.get_json()
    name = data.get('name')
    print(name)
    if not name:
        return jsonify({"status": 400, "success": False, "message": "Name is required"}), 400

    with driver.session() as session:
            # 通过name删除指定的club节点以及其所有关系
            query = (
                "MATCH (c:Club {name: $name}) "
                "DETACH DELETE c"
            )
            result = session.run(query, name=name)

            # 检查是否成功删除
            
            return jsonify({
                "status": 200,
                "success": True,
                "message": "删除成功",
            }), 200
            
# 获取俱乐部信息
@app.route('/api/clubInfo', methods=['POST'])
def getClubTeacherInfo():
    data = request.get_json()
    club_name = data.get('name')

    if not club_name:
        return jsonify({"status": 400, "success": False, "message": "Club name is required"}), 400

    try:
        with driver.session() as session:
            # 根据俱乐部名称查询Club节点和Person节点
            query = (
                "MATCH (c:Club {name: $clubName}) "
                "OPTIONAL MATCH (c)-[:HAS{role:$teacher}]->(p:Person) "
                "RETURN c, p.PersonName AS PersonName"
            )
            result = session.run(query, clubName=club_name,teacher="teacher")

            # 准备返回的数据结构
            club_info = None
            person_name = None
            for record in result:
                club_info = {key: value for key, value in record['c'].items()}
                person_name = record.get('PersonName', None)

            # 如果Club节点未找到，返回404
            if not club_info:
                return jsonify({
                    "status": 404,
                    "success": False,
                    "message": "Club not found"
                }), 404

            # 构建最终的返回数据
            final_data = {
                "Club": club_info,
                "TeacherName": person_name
            }

            return jsonify({
                "status": 200,
                "success": True,
                "message": "Club and teacher information retrieved successfully",
                "data": final_data
            }), 200

    except Exception as e:
        # 打印异常信息，用于调试
        print(str(e))
        # 返回500错误，表示服务器内部错误
        return jsonify({"status": 500, "success": False, "message": "An error occurred"}), 500
    
# 添加俱乐部成员
@app.route('/api/addclubmenber', methods=['POST'])
def addclubmember():
    data = request.get_json()
    club_name = data.get('name')
    PersonId = data.get('PersonId')

    with driver.session() as session:
            # 查找Club节点
            club_query = "MATCH (c:Club {name: $clubName}) RETURN c"
            club_result = session.run(club_query, clubName=club_name)
            club_node = None

            # 检查Club节点是否存在
            for record in club_result:
                club_node = record['c']
                break
            if not club_node:
                return jsonify({"status": 404, "success": False, "message": "Club not found"}), 404

            # 查找Person节点
            person_query = "MATCH (p:Person {PersonId: $personId}) RETURN p"
            person_result = session.run(person_query, personId=PersonId)
            person_node = None

            # 检查Person节点是否存在
            for record in person_result:
                person_node = record['p']
                break
            if not person_node:
                return jsonify({"status": 404, "success": False, "message": "Person not found"}), 404

            # 创建HAS关系
            relationship_query = "MATCH (c:Club), (p:Person) WHERE ID(c) = $clubId AND ID(p) = $personId CREATE (c)-[:HAS {role: 'student'}]->(p)"
            session.run(relationship_query, clubId=club_node.id, personId=person_node.id)

            return jsonify({"status": 200, "success": True, "message": "Club member relationship created successfully"}), 200

# 获取俱乐部成员信息
@app.route('/api/getclubmenber', methods=['POST'])
def getclubmember():
    data = request.get_json()
    club_name = data.get('name')

  
    with driver.session() as session:
        # 查询Club节点以及HAS关系指向的Person节点和对应的Photo节点的link属性
        query = (
            "MATCH (c:Club {name: $clubName})-[:HAS {role: 'student'}]->(p:Person)-[r:hasPhoto]->(ph:Photo) "
            "RETURN p, ph.link AS photoLink"
        )
        result = session.run(query, clubName=club_name)
        people_with_photos = []
        for record in result:
            person_node = record['p']
            photo_link = record['photoLink']
            person_data = {key: value for key, value in person_node.items()}
            person_data['photoLink'] = photo_link  # 添加Photo的link属性
            people_with_photos.append(person_data)
        # 检查people_with_photos列表是否为空
        if not people_with_photos:
            return jsonify({
                "status": 404,
                "success": False,
                "message": "No members found for the club or no photos available",
                "data": []
            }), 404
        # 返回包含Photo链接的Person节点信息
        return jsonify({
            "status": 200,
            "success": True,
            "message": "Members with photos retrieved successfully",
            "data": people_with_photos
        }), 200
# 删除俱乐部成员
@app.route('/api/deleteclubmenber', methods=['POST'])
def deleteclubmember():
    data = request.get_json()
    club_name = data.get('name')
    PersonId = data.get('PersonId')

   

    with driver.session() as session:
        # 删除Club和Person之间的HAS关系
        delete_relationship_query = (
            "MATCH (c:Club {name: $clubName})-[r:HAS]->(p:Person {PersonId: $PersonId}) "
            "DELETE r"
        )
        result = session.run(delete_relationship_query, clubName=club_name, PersonId=PersonId)
        # 获取操作统计信息
        
        return jsonify({
            "status": 200,
            "success": True,
            "message": "Club member relationship deleted successfully"
        }), 200

# 展示俱乐部成果

@app.route('/api/showclubresult', methods=['POST'])
def showclubresult():
    data = request.get_json()
    club_name = data.get('name')
    with driver.session() as session:
        # 第一步：找到与Club节点通过HAS关系连接的Person节点
        result = session.run(
            "MATCH (c:Club {name: $club_name})-[:HAS {role: 'teacher'}]->(p:Person)-[:PARTICIPATED_IN]->(comp:Competition ) "
            "WHERE comp.clubName = $club_name "
            "RETURN p, comp",
            {"club_name": club_name}
        )
        competition_list = []
        for record in result:
            person = record["p"]
            competition = record["comp"]
            
            # 初始化Competition对象，包含所有属性
            comp_dict = {k: v for k, v in competition.items()}
            print(comp_dict)
            # 第三步：为Competition节点添加HAS_ACHIEVEMENT信息
            has_achievement_result = session.run(
                "MATCH (comp:Competition)-[:HAS_ACHIEVEMENT]->(doc:Document) "
                "WHERE comp.id = $comp_id "
                "RETURN doc",
                {"comp_id": competition["id"]}
            )
            comp_dict["hasachievement"] = [{k: v for k, v in doc_record["doc"].items()} for doc_record in has_achievement_result]
            
            # 第四步：为Competition节点添加CompetitionAchievement信息
            achievement_result = session.run(    
                "MATCH (comp:Competition)-[:HAS_ACHIEVEMENT]->(comac:CompetitionAchievement) "
                "WHERE comp.id = $comp_id "
                "RETURN comac"
                ,{"comp_id": competition["id"]}
            )
            comp_dict["competitionachievement"] = [{k: v for k, v in achievement_record["comac"].items()} for achievement_record in achievement_result]


            # 第五步：为Competition节点添加chenguowendang信息
            evidence_document_result = session.run(
                "MATCH (comp:Competition)-[:HAS_ACHIEVEMENT]->(comac:CompetitionAchievement)-[:EVIDENCE]->(doc:Document) "
                "WHERE comp.id = $comp_id "
                "RETURN doc ",
                {"comp_id": competition["id"]}
            )
            # 由于可能有多个Document节点，我们使用列表来存储这些节点的信息
            if evidence_document_result:
                comp_dict["chenguowendang"] = [{k: v for k, v in doc_record["doc"].items()} for doc_record in evidence_document_result]

            # 第六步：为Competition节点添加photo信息
            evidence_photo_result = session.run(
                "MATCH (comp:Competition)-[:HAS_ACHIEVEMENT]->(comac:CompetitionAchievement)-[:EVIDENCE]->(photo:Photo) "
                "WHERE comp.id = $comp_id "
                "RETURN photo",
                {"comp_id": competition["id"]}
            )
            comp_dict["photo"] = [{k: v for k, v in photo_record["photo"].items()} for photo_record in evidence_photo_result]
            
            # 第七步：为Competition节点添加person信息
            evidence_person_result = session.run(
                "MATCH (comp:Competition)-[:HAS_ACHIEVEMENT]->(comac:CompetitionAchievement)-[:BELONG]->(p:Person) "
                "WHERE comp.id = $comp_id AND p.PersonRole <> 'teacher'"
                "RETURN p",
                {"comp_id": competition["id"],}
            )
            comp_dict["person"] = [{k: v for k, v in person_record["p"].items()} for person_record in evidence_person_result]
            # 第八步：为每个Person节点添加lunwen信息
            for person_dict in comp_dict["person"]:
                person_lunwen_result = session.run(
                    "MATCH  (doc:Document) -[:BELONG]->  (p:Person)"
                    "WHERE p.PersonId = $person_id  "
                    "RETURN doc",
                    {"person_id": person_dict["PersonId"]}
                )
                person_dict["lunwen"] = [{k: v for k, v in doc_record["doc"].items()} for doc_record in person_lunwen_result]
            # 第九步：为每个Person节点添加photo信息
            for person_dict in comp_dict["person"]:
                person_photo_result = session.run(
                    "MATCH (p:Person)-[:HAS_PHOTO]->(photo:Photo) "
                    "WHERE p.PersonId = $person_id  "
                    "RETURN photo",
                    {"person_id": person_dict["PersonId"]}
                )
                person_dict["photo"] = [{k: v for k, v in photo_record["photo"].items()} for photo_record in person_photo_result]
            
            competition_list.append(comp_dict)
    
    return jsonify({
        "status": 200,
        "success": True,
        "message": "Members with photos retrieved successfully",
        "data": competition_list
    }), 200
    
#查看自己俱乐部
@app.route('/api/competition/club', methods=['POST'])
def get_club():
    data = request.get_json()
    PersonId = data.get('PersonId')
    clubs_names = []
    with driver.session() as session:
        # 查找与Person节点通过HAS关系连接的Club节点的名称
        result = session.run(
            "MATCH (p:Club)-[:HAS]->(c:Person) "
            "WHERE c.PersonId = $PersonId "
            "RETURN p.name",
            {"PersonId": PersonId}
        )
        
        for record in result:
            clubs_names.append(record["p.name"])  # 只获取Club节点的name属性
            print(clubs_names)
    return jsonify({
        "status": 200,
        "success": True,
        "message": "Clubs retrieved successfully",
        "data": clubs_names
    }), 200

#添加班级
@app.route('/api/addclass', methods=['POST'])
def addClass():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    teacher = data.get('teacher')
    if not name or not description or not teacher:
        return jsonify({"status": 400, "success": False, "message": "name, description, and teacher are required"}), 400

    try:
        with driver.session() as session:
            # 创建club节点
            query_create_club = (
                "CREATE (c:Class {name: $name, description: $description, teacher: $teacher}) "
                "RETURN c"
            )
            result = session.run(query_create_club, name=name, description=description, teacher=teacher)
            club_node = dict(result.single()['c'].items())

            # 获取Class节点的ID
            club_id = club_node['name']

            # 创建Class-[HAS]-->person的关系
            query_create_relationship = (
                "MATCH (c:Class), (p:Person {PersonId: $teacher}) "
                "WHERE c.name = $clubId "
                "CREATE (c)-[:HAS {role:$role}]->(p)"
            )
            session.run(query_create_relationship, clubId=club_id, teacher=teacher,role="teacher")

        return jsonify({"status": 200, "success": True, "message": "Club created successfully", "data": club_node}), 200

    except Exception as e:
        # 打印异常信息，用于调试
        print(str(e))
        # 返回500错误，表示服务器内部错误
        return jsonify({"status": 500, "success": False, "message": "An error occurred"}), 500

#获取班级信息
@app.route('/api/getclass', methods=['GET'])
def getclass():
    try:
        with driver.session() as session:
            # 查询所有的Class节点
            query = "MATCH (c:Class) RETURN c"
            result = session.run(query)

            # 准备一个列表来存储查询结果
            clubs = []
            for record in result:
                club_node = dict(record['c'].items())
                clubs.append(club_node)

            # 返回包含所有Club节点的JSON数组
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Clubs retrieved successfully",
                "data": clubs
            }), 200

    except Exception as e:
        # 打印异常信息，用于调试
        print(str(e))
        # 返回500错误，表示服务器内部错误
        return jsonify({"status": 500, "success": False, "message": "An error occurred"}), 500

#删除班级
@app.route('/api/deleteclass', methods=['POST'])
def deleteclass():
    data = request.get_json()
    name = data.get('name')
    print(name)
    if not name:
        return jsonify({"status": 400, "success": False, "message": "Name is required"}), 400

    with driver.session() as session:
            # 通过name删除指定的club节点以及其所有关系
            query = (
                "MATCH (c:Class {name: $name}) "
                "DETACH DELETE c"
            )
            result = session.run(query, name=name)

            # 检查是否成功删除
            
            return jsonify({
                "status": 200,
                "success": True,
                "message": "删除成功",
            }), 200

#获取班级信息
@app.route('/api/getclasslist', methods=['POST'])
def getclasslist():
    data = request.get_json()
    club_name = data.get('name')

    if not club_name:
        return jsonify({"status": 400, "success": False, "message": "Club name is required"}), 400

    try:
        with driver.session() as session:
            # 根据俱乐部名称查询Club节点和Person节点
            query = (
                "MATCH (c:Class {name: $clubName}) "
                "OPTIONAL MATCH (c)-[:HAS{role:$teacher}]->(p:Person) "
                "RETURN c, p.PersonName AS PersonName"
            )
            result = session.run(query, clubName=club_name,teacher="teacher")

            # 准备返回的数据结构
            club_info = None
            person_name = None
            for record in result:
                club_info = {key: value for key, value in record['c'].items()}
                person_name = record.get('PersonName', None)

            # 如果Club节点未找到，返回404
            if not club_info:
                return jsonify({
                    "status": 404,
                    "success": False,
                    "message": "Club not found"
                }), 404

            # 构建最终的返回数据
            final_data = {
                "Club": club_info,
                "TeacherName": person_name
            }

            return jsonify({
                "status": 200,
                "success": True,
                "message": "Club and teacher information retrieved successfully",
                "data": final_data
            }), 200

    except Exception as e:
        # 打印异常信息，用于调试
        print(str(e))
        # 返回500错误，表示服务器内部错误
        return jsonify({"status": 500, "success": False, "message": "An error occurred"}), 500

#添加班级成员
@app.route('/api/addclassmenber', methods=['POST'])
def addclassmember():
    data = request.get_json()
    club_name = data.get('name')
    PersonId = data.get('PersonId')

    with driver.session() as session:
            # 查找Club节点
            club_query = "MATCH (c:Class {name: $clubName}) RETURN c"
            club_result = session.run(club_query, clubName=club_name)
            club_node = None

            # 检查Club节点是否存在
            for record in club_result:
                club_node = record['c']
                break
            if not club_node:
                return jsonify({"status": 404, "success": False, "message": "Club not found"}), 404

            # 查找Person节点
            person_query = "MATCH (p:Person {PersonId: $personId}) RETURN p"
            person_result = session.run(person_query, personId=PersonId)
            person_node = None

            # 检查Person节点是否存在
            for record in person_result:
                person_node = record['p']
                break
            if not person_node:
                return jsonify({"status": 404, "success": False, "message": "Person not found"}), 404

            # 创建HAS关系
            relationship_query = "MATCH (c:Class), (p:Person) WHERE ID(c) = $clubId AND ID(p) = $personId CREATE (c)-[:HAS {role: 'student'}]->(p)"
            session.run(relationship_query, clubId=club_node.id, personId=person_node.id)

            return jsonify({"status": 200, "success": True, "message": "Club member relationship created successfully"}), 200

# 获取班级成员信息
@app.route('/api/getclassmenber', methods=['POST'])
def getclassmember():
    data = request.get_json()
    club_name = data.get('name')

  
    with driver.session() as session:
        # 查询Club节点以及HAS关系指向的Person节点和对应的Photo节点的link属性
        query = (
            "MATCH (c:Class {name: $clubName})-[:HAS {role: 'student'}]->(p:Person)-[r:hasPhoto]->(ph:Photo) "
            "RETURN p, ph.link AS photoLink"
        )
        result = session.run(query, clubName=club_name)
        people_with_photos = []
        for record in result:
            person_node = record['p']
            photo_link = record['photoLink']
            person_data = {key: value for key, value in person_node.items()}
            person_data['photoLink'] = photo_link  # 添加Photo的link属性
            people_with_photos.append(person_data)
        # 检查people_with_photos列表是否为空
        if not people_with_photos:
            return jsonify({
                "status": 404,
                "success": False,
                "message": "No members found for the club or no photos available",
                "data": []
            }), 404
        # 返回包含Photo链接的Person节点信息
        return jsonify({
            "status": 200,
            "success": True,
            "message": "Members with photos retrieved successfully",
            "data": people_with_photos
        }), 200

# 删除班级成员
@app.route('/api/deleteclassmenber', methods=['POST'])
def deleteclassmember():
    data = request.get_json()
    club_name = data.get('name')
    PersonId = data.get('PersonId')

   

    with driver.session() as session:
        # 删除Club和Person之间的HAS关系
        delete_relationship_query = (
            "MATCH (c:Class {name: $clubName})-[r:HAS]->(p:Person {PersonId: $PersonId}) "
            "DELETE r"
        )
        result = session.run(delete_relationship_query, clubName=club_name, PersonId=PersonId)
        # 获取操作统计信息
        
        return jsonify({
            "status": 200,
            "success": True,
            "message": "Club member relationship deleted successfully"
        }), 200

#获取自己的班级
@app.route('/api/getmyclass', methods=['POST'])
def getmyclass():
    data = request.get_json()
    PersonId = data.get('PersonId')
    classes_list = []
    with driver.session() as session:
        # 查找与Person节点通过BELONGS_TO关系连接的Class节点
        result = session.run(
            "MATCH (c:Class)-[:HAS]->(p:Person) "
            "WHERE p.PersonId = $PersonId "
            "RETURN c",
            {"PersonId": PersonId}
        )
        
        for record in result:
            class_node = record["c"]
            # 将Class节点的所有属性添加到列表中
            class_dict = {k: v for k, v in class_node.items()}
            # print(class_dict)
            classes_list.append(class_dict)
    
    
    # 返回包含所有Class节点信息的JSON响应
    return jsonify({
        "status": 200,
        "success": True,
        "message": "Classes retrieved successfully",
        "data": classes_list
    }), 200

#教师发布作业
@app.route('/api/teacherpublish', methods=['POST'])
def teacherpublish():
    data = request.get_json()
    PersonId = data.get('PersonId')
    Class = data.get('Class')
    TestName = data.get('TestName')
    Important = data.get('Important')
    TestUrl = data.get('TestUrl')
    Aiwatch = data.get('Aiwatch')
    print(PersonId,Class,TestName,Important,TestUrl)
    with driver.session() as session:
        # 第一步：找到Class节点
        class_result = session.run(
            "MATCH (c:Class {name: $Class_name}) RETURN c",
            {"Class_name": Class}
        )
        class_record = class_result.single()
        if not class_record:
            return jsonify({"error": "Class not found"}), 404
        
        class_node = class_record["c"]
        
        # 第二步：创建HomeWork节点
        create_homework_query = (
            "CREATE (hw:HomeWork {TestUrl: $TestUrl, Important: $Important, TestName: $TestName, PersonId: $PersonId,Aiwatch:  $Aiwatch,alreadySubmit:0}) "
            "RETURN hw"
        )
        session.run(
            create_homework_query,
            {
                "TestUrl": TestUrl,
                "Important": Important,
                "TestName": TestName,
                "PersonId": PersonId,
                "Aiwatch": Aiwatch
            }
        )
        
        # 第三步：建立Class - BELONG - HomeWork关系
        create_relationship_query = (
            "MATCH (c:Class {name: $Class_name}), (hw:HomeWork {TestName: $TestName}) "
            "CREATE (c)-[:BELONG]->(hw) "
            "RETURN hw"
        )
        session.run(
            create_relationship_query,
            {
                "Class_name":Class ,
                "TestName": TestName
            }
        )
    
    # 返回成功的响应
    return jsonify({
        "status": 200,
        "success": True,
        "message": "Homework published successfully"
    }), 200
    
#学生获取作业
@app.route('/api/studentgetwork', methods=['POST'])
def studentgetwork():
    data = request.get_json()
    PersonId = data.get('PersonId')
    Class_name = data.get('Class')
    
    homework_list = []
    with driver.session() as session:
        # 第一步：找到Class节点
        class_result = session.run(
            "MATCH (c:Class {name: $Class_name}) RETURN c",
            {"Class_name": Class_name}
        )
        class_record = class_result.single()
        if not class_record:
            return jsonify({"error": "Class not found"}), 404
        
        # 第二步：从Class节点查找每个HomeWork节点
        unsubmitted_query = (
            "MATCH (c:Class {name: $Class_name})-[:BELONG]->(hw:HomeWork) "
            "WHERE NOT EXISTS ((hw)-[:SUBMIT]->(:SubmitWork {stuId: $PersonId})) "
            "RETURN hw"
        )
        unsubmitted_homeworks = session.run(unsubmitted_query, {"Class_name": Class_name, "PersonId": PersonId})
        
        for record in unsubmitted_homeworks:
            homework_node = record["hw"]
            # 将HomeWork节点的所有属性添加到列表中
            homework_list.append({k: v for k, v in homework_node.items()})
    # print(homework_list)
    # 返回未提交的HomeWork节点信息数组
    return jsonify({
        "status": 200,
        "success": True,
        "message": "Unsubmitted homework retrieved successfully",
        "data": homework_list
    }), 200
#学生提交作业
@app.route('/api/submitworkApi', methods=['POST'])
def studentsubmitwork():
    data = request.get_json()
    Aiwatch = data.get('Aiwatch')
    TestName = data.get('TestName')
    fileList = data.get('fileList')  #文件/我的作业
    place = data.get('place') # 备注
    Class = data.get('Class')
    stuId = data.get('stuId')
    Important = data.get('Important')  #Ai关键词
    TestUrl = data.get('TestUrl')    #作业连接
    PersonId = data.get('PersonId')
    alreadySubmit = data.get('alreadySubmit')
    
    if Aiwatch is False:
        with driver.session() as session:
            query = (
                "MATCH (c:Class {name: $Class_name})-[:BELONG]->(hw:HomeWork) "
                "WHERE hw.TestName = $TestName "
                "WITH hw "
                "MERGE (hw)-[:SUBMIT ]->(sw:SubmitWork {Aiwatch: $Aiwatch, fileList: $fileList, place: $place, teacher: $PersonId,  stuId:$stuId,flag:'ing'}) "
                "SET hw.alreadySubmit = coalesce(hw.alreadySubmit, 0) + 1 "
                "RETURN sw"
            )
            result = session.run(query, {
                "Class_name": Class,
                "TestName": TestName,
                "PersonId": PersonId,
                "Aiwatch": Aiwatch,
                "fileList": fileList,
                "place": place,
                "stuId": stuId,
            })

            
            submit_work_record = result.single()
            if submit_work_record:
                submit_work = submit_work_record["sw"]
                submit_work_dict = {
                    "Aiwatch": submit_work.get("Aiwatch"),
                    "fileList": submit_work.get("fileList"),
                    "place": submit_work.get("place"),
                    "teacher": submit_work.get("teacher"),
                    "stuId": submit_work.get("stuId"),
                    "flag": submit_work.get("flag"),
                }

            # 返回成功的响应
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Submission successful",
                "data": submit_work_dict
            }), 200

    else:
        ohoto = submitFile(fileList,place,Important,TestUrl,TestName)
        print(ohoto['aiask'] ,ohoto['award'])
        if(ohoto['award']>60):
            with driver.session() as session:
                query = (
                    "MATCH (c:Class {name: $Class_name})-[:BELONG]->(hw:HomeWork) "
                    "WHERE hw.TestName = $TestName "
                    "WITH hw "
                    "MERGE (hw)-[:SUBMIT ]->(sw:SubmitWork {Aiwatch: $Aiwatch, fileList: $fileList, place: $place, teacher: $PersonId,  stuId:$stuId,   flag:'ing',aiask:$aiask,award:$award}) "
                    "SET hw.alreadySubmit = coalesce(hw.alreadySubmit, 0) + 1 "
                    "RETURN sw"
                )
                result = session.run(query, {
                    "Class_name": Class,
                    "TestName": TestName,
                    "PersonId": PersonId,
                    "Aiwatch": Aiwatch,
                    "fileList": fileList,
                    "place": place,
                    "stuId": stuId,
                    "aiask": ohoto['aiask'],
                    "award": ohoto['award'],
                })
                submit_work_record = result.single()
                if submit_work_record:
                    submit_work = submit_work_record["sw"]
                    submit_work_dict = {
                        "Aiwatch": submit_work.get("Aiwatch"),
                        "fileList": submit_work.get("fileList"),
                        "place": submit_work.get("place"),
                        "teacher": submit_work.get("teacher"),
                        "stuId": submit_work.get("stuId"),
                        "flag": submit_work.get("flag"),
                        "aiask": submit_work.get("aiask"),
                        "award": submit_work.get("award"),
                    }
                return jsonify({
                "status": 200,
                "success": True,
                "message": "Submission successful",
                "data": submit_work_dict
                }), 200

        else:
            submit_work_dict = {
            "aiask": ohoto['aiask'],
            "award": ohoto['award'],
            }
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Submission successful",
                "data": submit_work_dict
                }), 200
        
        

#学生继续提交
@app.route('/api/continueSubmit', methods=['POST'])
def continueSubmit():
    data = request.get_json()
    data = request.get_json()
    Aiwatch = data.get('Aiwatch')
    TestName = data.get('TestName')
    fileList = data.get('fileList')  #文件/我的作业
    place = data.get('place') # 备注
    Class = data.get('Class')
    stuId = data.get('stuId')
    Important = data.get('Important')  #Ai关键词
    TestUrl = data.get('TestUrl')    #作业连接
    PersonId = data.get('PersonId')
    alreadySubmit = data.get('alreadySubmit')
    aiask = data.get('aiask')
    award = data.get('award')

    with driver.session() as session:
            query = (
                "MATCH (c:Class {name: $Class_name})-[:BELONG]->(hw:HomeWork) "
                "WHERE hw.TestName = $TestName "
                "WITH hw "
                "MERGE (hw)-[:SUBMIT ]->(sw:SubmitWork {Aiwatch: $Aiwatch, fileList: $fileList, place: $place, teacher: $PersonId,  stuId:$stuId,flag:'ing',aiask:$aiask,award:$award}) "
                "SET hw.alreadySubmit = coalesce(hw.alreadySubmit, 0) + 1 "
                "RETURN sw"
            )
            result = session.run(query, {
                "Class_name": Class,
                "TestName": TestName,
                "PersonId": PersonId,
                "Aiwatch": Aiwatch,
                "fileList": fileList,
                "place": place,
                "stuId": stuId,
                "aiask": aiask,
                "award": award,
            })
            submit_work_record = result.single()
            if submit_work_record:
                submit_work = submit_work_record["sw"]
                submit_work_dict = {
                    "Aiwatch": submit_work.get("Aiwatch"),
                    "fileList": submit_work.get("fileList"),
                    "place": submit_work.get("place"),
                    "teacher": submit_work.get("teacher"),
                    "stuId": submit_work.get("stuId"),
                    "flag": submit_work.get("flag"),
                    "aiask": submit_work.get("aiask"),
                    "award": submit_work.get("award"),
                }
    
    return jsonify({
                "status": 200,
                "success": True,
                "message": "Submission successful",
                "data": submit_work_dict
            }), 200
        
    

#学生获取历史作业
@app.route('/api/gethistoryworklist', methods=['POST'])
def gethistoryworklist():
    data = request.get_json()
    PersonId = data.get('PersonId')
    Class_name = data.get('Class')

    history_work_list = []
    with driver.session() as session:
        # 查询Class节点、Person节点、HomeWork节点和相关的SubmitWork节点
        homework_query = (
            "MATCH (p:Person {PersonId: $PersonId})<-[:HAS]-(c:Class {name: $Class_name})-[:BELONG]->(hw:HomeWork) "
            "OPTIONAL MATCH (hw)-[r:SUBMIT]->(sw:SubmitWork {stuId: $PersonId}) "
            "RETURN hw, r, sw"
        )
        result = session.run(homework_query, {
            "PersonId": PersonId,
            "Class_name": Class_name
        })

        # 构建最终结果
        for record in result:
            homework = record["hw"]
            submit_work = record["sw"]
            if(submit_work is not None):
                history_work = {
                    "HomeWork": {
                        "Aiwatch": homework.get("Aiwatch"),
                        "Important": homework.get("Important"),
                        "PersonId": PersonId,
                        "TestName": homework.get("TestName"),
                        "TestUrl": homework.get("TestUrl"),
                        "alreadySubmit": homework.get("alreadySubmit")
                    },
                    "SubmitWork": {
                        "fileList": submit_work.get("fileList") if submit_work else None,
                        "place": submit_work.get("place") if submit_work else None,
                        "stuId": submit_work.get("stuId") if submit_work else None,
                        "flag": submit_work.get("flag") if submit_work else None
                    }
                }
                history_work_list.append(history_work)
    print(history_work_list)
    # 返回历史作业列表
    return jsonify({
        "status": 200,
        "success": True,
        "message": "History work list retrieved successfully",
        "data": history_work_list
    }), 200

#教师获取历史作业
@app.route('/api/Teachergethistoryworklist', methods=['POST'])
def Teachergethistoryworklist():
    data = request.get_json()
    PersonId = data.get('PersonId')
    Class_name = data.get('Class')

    homework_list = []
    student_count = 0
    with driver.session() as session:
        # 查找特定的Class节点
        class_query = (
            "MATCH (c:Class {name: $Class_name})-[:HAS {role: 'teacher'}]->(p:Person {PersonId: $PersonId}) "
            "RETURN c"
        )
        class_result = session.run(class_query, {
            "Class_name": Class_name,
            "PersonId": PersonId
        })
        class_record = class_result.single()
        if not class_record:
            return jsonify({
                "status": 404,
                "success": False,
                "message": "Class not found"
            }), 404

        # 基于确定的Class节点统计role为'student'的Person节点数量
        student_query = (
            "MATCH (c:Class {name: $Class_name})-[:HAS {role: 'student'}]->(p:Person) "
            "RETURN count(p) as studentCount"
        )
        student_result = session.run(student_query, {
            "Class_name": Class_name
        })
        student_count = student_result.single()["studentCount"]

        # 获取所有HomeWork节点的属性
        homework_query = (
            "MATCH (c:Class {name: $Class_name})-[:BELONG]->(hw:HomeWork) "
            "RETURN hw"
        )
        homework_result = session.run(homework_query, {
            "Class_name": Class_name
        })

        # 构建HomeWork节点属性的对象数组
        for record in homework_result:
            homework = record["hw"]
            homework_dict = {
                "Aiwatch": homework.get("Aiwatch"),
                "Important": homework.get("Important"),
                "PersonId": homework.get("PersonId"),
                "TestName": homework.get("TestName"),
                "TestUrl": homework.get("TestUrl"),
                "alreadySubmit": homework.get("alreadySubmit")
            }
            homework_list.append(homework_dict)

    # 返回HomeWork节点属性的对象数组和学生数量
    return jsonify({
        "status": 200,
        "success": True,
        "message": "History work list retrieved successfully",
        "data": {
            "homework_list": homework_list,
            "student_count": student_count
        }
    }), 200

#教师获取某历史作业的学生提交内容
@app.route('/api/Teachergethistorywork', methods=['POST'])
def Teachergethistorywork():
    data = request.get_json()
    PersonId = data.get('PersonId')
    Class_name = data.get('Class')
    TestName = data.get('TestName')

    submit_work_list = []
    with driver.session() as session:
        # 查找特定的Class节点
        class_query = (
            "MATCH (c:Class {name: $Class_name})-[:HAS {role: 'teacher'}]->(p:Person {PersonId: $PersonId}) "
            "WITH c "
            "MATCH (c)-[:BELONG]->(hw:HomeWork {TestName: $TestName}) "
            "MATCH (hw)-[:SUBMIT]->(sw:SubmitWork) "
            "RETURN sw"
        )
        result = session.run(class_query, {
            "Class_name": Class_name,
            "PersonId": PersonId,
            "TestName": TestName
        })

        # 构建SubmitWork节点属性的对象数组
        for record in result:
            submit_work = record["sw"]
            submit_work_dict = {
                "fileList": submit_work.get("fileList"),
                "place": submit_work.get("place"),
                "stuId": submit_work.get("stuId"),
                "flag": submit_work.get("flag"),
                "aiask":submit_work.get("aiask"),
                "award": submit_work.get("award"),
                "teacherAsk":submit_work.get("teacherAsk"),
                "teacherScore": submit_work.get("teacherScore"),
            }
            
            # 查询对应的Person节点信息
            person_query = (
                "MATCH (p:Person {PersonId: $stuId}) "
                "RETURN p"
            )
            person_result = session.run(person_query, {
                "stuId": submit_work.get("stuId")
            })
            person_record = person_result.single()
            if person_record:
                person_info = {
                    "PersonId": person_record["p"].get("PersonId"),
                    "PersonName": person_record["p"].get("PersonName"),
                    "PersonRole": person_record["p"].get("PersonRole")
                }
                submit_work_dict["PersonInfo"] = person_info
            
            submit_work_list.append(submit_work_dict)

    # 返回SubmitWork节点属性的对象数组
    return jsonify({
        "status": 200,
        "success": True,
        "message": "Submit work list retrieved successfully",
        "data": submit_work_list
    }), 200

#老师批改作业
@app.route('/api/grade_work', methods=['POST'])
def grade_work():
    data = request.get_json()
    class_Name = data.get('class')
    PersonId = data.get('PersonId')
    TestName = data.get('TestName')
    stuId = data.get('stuId')
    teacherAsk = data.get('teacherAsk')
    teacherScore = data.get('teacherScore')
    print(teacherAsk,teacherScore)
    with driver.session() as session:
        query = (
            "MATCH (c:Class {name: $class_Name})-[:HAS]->(p:Person {PersonId: $PersonId}) "
            "MATCH (c)-[:BELONG]->(hw:HomeWork {TestName: $TestName}) "
            "MATCH (hw)-[:SUBMIT]->(sw:SubmitWork {stuId: $stuId}) "
            "SET sw.flag = 'true', sw.teacherAsk = $teacherAsk, sw.teacherScore = $teacherScore "
            "RETURN sw"
        )
        result = session.run(query, {
            "class_Name": class_Name,
            "PersonId": PersonId,
            "TestName": TestName,
            "stuId": stuId,
            "teacherAsk": teacherAsk,
            "teacherScore": teacherScore
        })

        # 获取更新后的SubmitWork节点信息
        submit_work_record = result.single()
        if submit_work_record:
            submit_work = submit_work_record["sw"]
            submit_work_dict = {
                "flag": submit_work.get("flag"),
                "teacherAsk": submit_work.get("teacherAsk"),
                "teacherScore": submit_work.get("teacherScore")
            }
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Grading successful",
                "data": submit_work_dict
            }), 200
        else:
            return jsonify({
                "status": 404,
                "success": False,
                "message": "SubmitWork not found"
            }), 404
    

if __name__ == '__main__':
    print('starting app')
    app.run(host='0.0.0.0', port=5000)
    