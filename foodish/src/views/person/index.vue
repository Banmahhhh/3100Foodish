<template>
  <div class="person">
    <div class="person-header">
      <div class="person-left" @click="$router.push({ name: 'Home' })">
        <img src="@/resource/fanhui.svg" alt="" />
      </div>
      <span>Foodish</span>
    </div>
    <div class="person-main-form">
      <div class="person-main-left">
        <ul>
          <li :class="{ active: active === 0 }" @click="onClickMenu(0)">
            Accout Information
          </li>
          <li :class="{ active: active === 1 }" @click="onClickMenu(1)">
            I have bought
          </li>
          <li :class="{ active: active === 2 }" @click="onClickMenu(2)">
            I have cooked
          </li>
          <li :class="{ active: active === 3 }" @click="onClickMenu(3)">
            Comming order
          </li>
          <li :class="{ active: active === 4 }" @click="onClickMenu(4)">
            Private message
          </li>
        </ul>
      </div>
      <div v-if="active === 0" class="person-main-right">
        <!-- user -->
        <div class="person-main-row">
          <div class="person-logo">
            <div :style="getCurrStyle()" class="person-image"></div>
            <Upload :on-success="onFileSuccess" name="img" :show-upload-list="false" multiple type="drag" :action="API.IMAGE_UPLOAD">
              <Button size="small">change</Button>
            </Upload>

          </div>
          <div class="person-info">
            <Rate :value="score" disabled />
            <p style="font-size:20px">{{uname}}</p>
            <p style="font-size:20px">{{username}}</p>
            <p style="font-size:20px">fans:{{fans_num}}</p>
            <br><br>
            <Input v-model="last_name" type="textarea" :autosize="{minRows: 3,maxRows:10}" placeholder="Enter desc...">

            </Input>
            <br><br>
            <Button @click="onDescChange" size="small">change</Button>
          </div>
        </div>
        <!-- loginout -->
        <div class="person-main-row-btn">
          <Button @click="logout" type="warning" class="logout" size="large">logout</Button>
        </div>
      </div>
      <div v-if="active === 1" class="person-main-right" style="padding-top:0">
        <div class="not-data" v-if="bookList2.length === 0">
          <img src="../../resource/745077899322453353.jpg" />
          <p>It is empty. Add something to it now!</p>
        </div>
        <FoodItemSmall @evaluate="onEvaluate" commit :align="`${index % 2 !== 0 ? 'right' : 'left'}`" v-for="(item, index) in bookList2" :key="item.id" :item="item.food_detail" :isCommit="item.is_comment" />
      </div>
      <div v-if="active === 2" class="person-main-right" style="padding-top:0">
        <div class="not-data" v-if="foodListSoon.length === 0">
          <img src="../../resource/745077899322453353.jpg" />
          <p>It is empty. Add something to it now!</p>
        </div>
        <FoodItemSmall :align="`${index % 2 !== 0 ? 'right' : 'left'}`" v-for="(item, index) in foodListSoon" :key="item.id" :item="item" />
      </div>
      <div v-if="active === 3" class="person-main-right" style="padding-top:0">
        <div class="not-data" v-if="commingList.length === 0">
          <img src="../../resource/745077899322453353.jpg" />
          <p>It is empty. Add something to it now!</p>
        </div>
        <FoodItemSmall comming :align="`${index % 2 !== 0 ? 'right' : 'left'}`" v-for="(item, index) in commingList" :key="item.id" :item="item" />
      </div>
      <div v-if="active === 4" class="person-main-right" style="padding-top:0">
        <Notify v-for="(item, index) in messageList" :key="item.id" :item="item" />
      </div>
    </div>
    <!-- 评论 -->
    <Modal :value="isCommit" @on-cancel="isCommit = false" title="evaluate" :styles="{ width: '500px' }">
      <div class="modal-wrap">
        <div class="modal-inner">
          <div class="image" :style="currStyle(modal.image_url)"></div>
          <div class="right">
            <p>{{ modal.name }}</p>
            <p>{{ modal.date | dateFormat("yyyy-MM-dd hh:mm") }}</p>
          </div>
        </div>
        <Rate v-model="modal.score" />
        <Input type="textarea" v-model="modal.content" :rows="4" placeholder="commit"></Input>
      </div>
      <div slot="footer" class="modal-footer">
        <Button @click="isCommit = false">cancel</Button>
        <Button @click="isReport=true,isCommit=false" style="color:red">report</Button>
        <Button @click="onCommitAdd" type="warning">ok</Button>
      </div>
    </Modal>
    <!-- 举报 -->
    <Modal :value="isReport" @on-cancel="isReport = false" title="evaluate" :styles="{ width: '500px' }">
      <div class="modal-wrap">
        <p>report reason</p>
        <Row :gutter="16">
          <Col :span="14">
          <Input type="textarea" v-model="reportForm.text" :rows="14" placeholder="commit"></Input>
          </Col>
          <Col :span="10">
          <Upload :on-success="onFileSuccess2" name="img" :show-upload-list="false" multiple type="drag" :action="API.IMAGE_UPLOAD">
            <div v-if="!reportForm.image_url" style="padding: 120px 0">
              <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
            </div>
            <div v-else :style="`background:url(${reportForm.image_url}) no-repeat top center;
                background-size: cover;width:100%;height:300px`">
            </div>
          </Upload>
          </Col>
        </Row>
      </div>
      <div slot="footer" class="modal-footer">
        <Button @click="isReport = false">cancel</Button>
        <Button @click="onReport" type="warning">commit</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import FoodItemSmall from "@/components/FoodItemSmall";
import Notify from '@/components/Notify'
export default {
  components: { FoodItemSmall ,Notify},
  data() {
    return {
      reportForm:{
          image_url:"",
          text:"",
          food:""
      },  
      isReport:false,
      last_name:"",
      active: 0,
      commitId: "",
      isCommit: false,
      image_url: "",
      score: 0,
      modal: {
        id: "",
        name: "",
        date: "",
        image_url: "",
        score: 0,
        content: ""
      },
      forms: {},
      rules: {},
      flavorList: [],
      dislikeList: [],
      bookList: [],
      commitList: [],
      messageList:[],
      foodList: [] //我做的菜列表
    };
  },
  computed: {
    fans_num(){
      return this.$store.state.users.fans_num;
    },
    uname(){
      return this.$store.state.users.name;
    },
    username() {
      return this.$store.state.users.username;
    },
    bookList2(){
      return this.bookList.filter(item=>item.date<+new Date())
    },
    foodListSoon(){
        return this.foodList.filter(item=>item.date<+new Date()).filter(item=>!item.is_cancel)
    },
    commingList() {
      const d = +new Date();
      const dayTime = 24 * 60 * 60 * 1000;
      const list = [...this.foodList,...this.bookList]
      return this.bookList
        .map(item => {
          const food_detail = item.food_detail;
          if (food_detail) {
            if (d - food_detail.date <= dayTime && !food_detail.is_cancel) {
              return {
                ...item,
                ...food_detail,
                orderStatus: 0,
                orderText: "You need to take it"
              };
            }

            if (food_detail.is_cancel) {
              return {
                ...item,
                ...food_detail,
                orderStatus: 1,
                orderText: "It has been canceled"
              };
            }

            //
          }
        })
        .concat(this.foodList)
        .map((item)=>{
          const text="you need to cook it"
          if (!item.is_cancel) {
              return {
                ...item,
                
                orderStatus: 0,
                orderText:this.$store.state.users.id==item.author?text: "You need to take it"
              };
            }

            if (item.is_cancel) {
              return {
                ...item,
                
                orderStatus: 1,
                orderText: "It has been canceled"
              };
            }
        })
        .filter(item => {
          if(+new Date()<=item.date) {
            return true
          }
          return false;
        });
    }
  },
  created() {
    this.flavorList = this.$utils.flavor;
    this.dislikeList = this.$utils.dislike;
    this.getBookInfo();
    this.getFoodList();
    this.getUserInfo();
    this.getUserNotify()
  },
  methods: {
    async onDescChange(){
      console.log(this.$store.state.users)
      await this.$http({
        url:this.API.UPDATE_USER( this.$store.state.users.id),
        method: "PATCH",
        data:{
          last_name:this.last_name
        }
      })
      this.$Message.success("edit successfully");
      this.getUserInfo()
    },
    async getUserNotify(){
        const {data}= await this.$http({
            url:this.API.NOTIFY,
            params:{
                listener:this.$store.state.users.id,
            }
        })
        this.messageList = data
    },
    currStyle(img) {
      return `background-image:url(${img});width:150px;height:100px;`;
    },
    getCurrStyle() {
      return `background-image:url(${
        this.image_url
      });background-size: cover;width:100%;height:200px;background-color:#eee;background-size: cover;`;
    },
    async getCommitList() {
      const { data } = await this.$http({
        url: this.API.COMMIT_ADD,
        params: {
          auther: this.$store.state.users.id
        }
      });
      let score = 0;
      this.foodListSoon.map(item => {
        score += item.score;
      });
      this.score = score / data.length;
      this.commitList = data;
    },
    async getUserInfo() {
      const { data } = await this.$http({
        url: this.API.UPDATE_USER(this.$store.state.users.id),
        method: "get"
      });
      this.$store.commit("users", Object.assign(this.$store.state.users, data));
      this.image_url = data.image_url;
      this.last_name = data.last_name;
    },
    async onFileSuccess(res) {
      await this.$http({
        url: this.API.UPDATE_USER(this.$store.state.users.id),
        method: "PATCH",
        data: {
          image_url: res.url
        }
      });
      this.getUserInfo();
    },
    async onFileSuccess2(res){
        this.reportForm.image_url = res.url
    },
    async getFoodList() {
      const { data } = await this.$http({
        url: this.API.FOOD_LIST,
        params: {
          author: this.$store.state.users.id
        }
      });
      this.foodList = data.sort((a, b) => {
        if (a.date > b.date) {
          return -1;
        } else {
          return 1;
        }
      });
      this.getCommitList();
    },
    async getBookInfo() {
      const { data } = await this.$http({
        url: this.API.BOOK_LIST_Q(this.$store.state.users.id)
      });
      this.bookList = data.map(item => {
        if (item.food_detail) {
          item.food_detail = JSON.parse(item.food_detail);
          item.date = item.food_detail.date
        }
        return item;
      });
    },
    onClickMenu(active) {
      this.active = active;
    },
    logout() {
      this.$store.commit("users", {});
      this.$router.replace({ name: "Login" });
    },
    onEvaluate(item) {
      this.isCommit = true;
      this.modal = Object.assign(this.modal, {
        image_url: item.image_url,
        name: item.name,
        date: item.date,
        score: 0,
        content: "",
        id: item.id
      });
      this.reportForm.food = item.id
      this.reportItem = item
      this.reportForm.text = ""
      this.reportForm.image_url = ""
      console.log(this.reportItem)
    },
    async onCommitAdd() {
      await this.$http({
        url: this.API.COMMIT_ADD,
        method: "post",
        data: {
          description: this.modal.content,
          score: this.modal.score,
          auther: this.$store.state.users.id,
          food: this.modal.id
        }
      });
      this.isCommit = false;
      //刷新列表
      this.getBookInfo();
      this.$Message.success("Evaluation success!");
    },
    async onReport(){
        if(!this.reportForm.text){
            return this.$Message.info("Please enter complaints")
        }
        const foodInfo = {}
        Object.keys(this.reportItem).map(key=>{
            foodInfo['_'+key] = this.reportItem[key]
        })
        await this.$http({
        url: this.API.COMPLAIN,
        method: "post",
        data: {
          text: this.reportForm.text,
          user_detail: JSON.stringify({
              ...this.$store.state.users,
              ts_image_url:this.reportForm.image_url,
              ...foodInfo
          }),
          creater: this.$store.state.users.id,
          food: this.reportForm.food,
        }
      });
      this.isReport = false;
      //刷新列表
      this.getBookInfo();
      this.$Message.success("Report success!");
    }
  }
};
</script>

<style lang="less">
@import "./style.less";
</style>
<style lang="less" >
</style>

