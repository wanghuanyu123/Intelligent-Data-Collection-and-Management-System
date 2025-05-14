<template>
    <div>
      <div id="sonHiddenIcon" class="son_icon son_icon_hideen" @click="btn_display_icon">
        >
      </div>
      <div class="left_layout" :style="{ display: leftLayoutDisplay }">
        <div class="father_icon">
          <div id="sonIcon" class="son_icon son_icon_display" @click="btn_icon">
            
          </div>
          <div id="left_person" class="left_person">
            <div style="display:flex;justify-content: center;align-items:center">
              <div class="false_img">
                <div class="flase_img_son"></div>
              </div>
              <div class="false_img_right">
                <strong>Michael Jackson</strong>
              </div>
            </div>
          </div>
        </div>
        <div class="new_chat">新建聊天</div>
        <div class="new_chat new_chat_text">
          <div class="false_img" style="border:1px solid lightgray;border-radius:20%;color:green;">...</div>
          <div style="flex:8;color:green;">前端有哪些性能优化？</div>
        </div>
      </div>
      <div class="right_layout">
        <div class="right_layout_son">
          <div class="right_layout_myselfChat">
            <div :style="{ color: timeColor }" style="flex:2;font-size:13px">{{ dateTime }}</div>
            <div style="flex:1">
              <div class="flase_img_son" style="width:40px;height:40px;"></div>
            </div>
          </div>
          <div class="myself_chat">
            前端有哪些性能优化？
          </div>
          <div class="right_layout_son_ipt">
            <input class="ipt" type="text" placeholder="来说点什么吧...">
            <button class="btn">发送</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const leftLayoutDisplay = ref('block');
  const sonIcon = ref(null);
  const hiddenSonIcon = ref(null);
  const dateTime = ref('');
  
  const btn_icon = () => {
    leftLayoutDisplay.value = 'none';
    hiddenSonIcon.value.style.display = 'block';
  };
  
  const btn_display_icon = () => {
    leftLayoutDisplay.value = 'block';
    hiddenSonIcon.value.style.display = 'none';
  };
  
  const isZero = (num) => (num < 10 ? '0' : '') + num;
  
  const getDateTime = () => {
    const datetime = new Date();
    const year = datetime.getFullYear();
    const month = isZero(datetime.getMonth() + 1);
    const day = isZero(datetime.getDate());
    const hour = isZero(datetime.getHours());
    const minute = isZero(datetime.getMinutes());
    const seconds = isZero(datetime.getSeconds());
    const date = `${year}/${month}/${day} ${hour}:${minute}:${seconds}`;
    return date;
  };
  
  dateTime.value = getDateTime();
  
  // Update date time every second
  setInterval(() => {
    dateTime.value = getDateTime();
  }, 1000);
  </script>
  
  <style>
  /* 将原有的 CSS 样式放在这里 */
  * {
				margin: 0;
				padding: 0;
				outline: none;
				box-sizing: border-box;
			}

			body {
				margin: 1vh 20px;
				min-height: 98vh;
				display: flex;
				justify-content: center;
				align-content: center;
				/* border: 1px solid lightgray; */
				box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px, rgba(0, 0, 0, 0.3) 0px 8px 16px -8px;
			}

			.left_layout {
				flex: 1;
				border-right: 1px solid lightgray;
			}

			.right_layout {
				flex: 6;
			}

			.father_icon {
				position: relative;
			}

			.son_icon {
				background-color: white;
				z-index: 99;
				position: absolute;
				font-size: 20px;
				border-radius: 50%;
				border: 1px solid lightgray;
				padding: 0px 5px;
				box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px, rgba(0, 0, 0, 0.3) 0px 8px 16px -8px;
				color: gray;
			}

			.son_icon_display {
				top: 48vh;
				right: -15px;
			}

			.son_icon_hideen {
				top: 48vh;
				left: 10px;
				display: none;
			}

			.new_chat {
				border: 1px solid lightgray;
				padding: 10px 20px;
				margin: 20px 10px;
				text-align: center;
			}

			.new_chat_text {
				border: 1px solid green;
				display: flex;
			}

			.left_person {
				width: 100%;
				padding: 1vh 20px;
				/* margin:20px 10px; */
				position: absolute;
				top: 90vh;
				border-top: 1px solid lightgray;
			}

			.false_img {
				/* background:linear-gradient(-135deg,#0c80cc,#009dff); */
				flex: 1;
			}

			.false_img_right {
				flex: 3;
			}

			.flase_img_son {
				width: 50px;
				height: 50px;
				background: linear-gradient(-135deg, #0000cc, #009dff);
				border: 1px solid lightblue;
				border-radius: 50%;
			}
		
			.right_layout_flex{
				display:flex;
				justify-content: center;
				align-items: center;
			}
			.right_layout_son{
				margin:0 auto 0 auto;
				width:100vh;
				height:98vh;
				/* border:1px solid gray; */
				position: relative;
			}
			.right_layout_son_ipt{
				position: absolute;
				bottom:0;
			}
			.btn{
				border:none;
				padding:10px 15px;
				background-color: #18a058;
				border-radius: 1px;
				color:white;
			}
			.ipt{
				width:85vh;
				margin:10px 20px;
				padding:10px 20px;
				border:1px solid lightgray;
			}
			.right_layout_myselfChat{
				width:200px;
				position: absolute;
				top:5px;
				right:0;
				display:flex;
			}
			.myself_chat{
				position: absolute;
				top:30px;
				right:80px;
				padding:10px 20px;
				border-radius: 10px;
				background-color: #7ae1b6;
				opacity: 0.8;
			}

  </style>