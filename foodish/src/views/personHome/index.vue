<template>
  <div class="person">
    <div class="person-header">
      <div class="person-left" @click="$router.push({ name: 'Home' })">
        <img src="@/resource/fanhui.svg" alt="" />
      </div>
      <span>Foodish</span>
    </div>
    <div class="person-main-form">
      <div class="person-main-right" style="padding:40px;width:100%">
        <!-- user -->
        <div class="person-main-row">
          <div class="person-logo">
            <div :style="getCurrStyle()" class="person-image"></div>
          </div>
          <div class="person-info">
            <Rate :value="score" disabled />
            <p style="font-size:20px">{{ uname }}</p>
            <p style="font-size:20px">{{ username }}</p>
            <p style="font-size:20px">fans:{{fans_num}}</p>
            <p style="font-size:14px">{{last_name}}</p>
            <p>
              <Button type="warning" size="small" @click="onFollow(is_follow)">{{is_follow?'cancel follow':'follow'}}</Button>
            </p>
          </div>
        </div>
        <div style="padding-top:0">
          <div class="not-data" v-if="foodList.length === 0">
            <img src="../../resource/745077899322453353.jpg" />
            <p>It is empty. Add something to it now!</p>
          </div>
          <FoodItemSmall :align="`${index % 2 !== 0 ? 'right' : 'left'}`" v-for="(item, index) in foodList" :key="item.id" :item="item" />
        </div>
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
        <Button @click="onCommitAdd" type="warning">ok</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import FoodItemSmall from "@/components/FoodItemSmall";
export default {
  components: { FoodItemSmall },
  data() {
    return {
      active: 0,
      commitId: "",
      isCommit: false,
      image_url: "",
      last_name:"",
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
      is_follow: false,
      rules: {},
      user: {},
      flavorList: [],
      dislikeList: [],
      bookList: [],
      commitList: [],
      foodList: [] //我做的菜列表
    };
  },
  computed: {
    fans_num() {
      return this.user.fans_num;
    },
    uname(){
      return this.user.name;
    },
    username() {
      return this.user.username;
    },
    commingList() {
      const d = +new Date();
      const dayTime = 24 * 60 * 60 * 1000;
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
        .filter(item => {
          return +new Date() >= item.date && item.is_cancel;
        });
    }
  },
  async created() {
    this.flavorList = this.$utils.flavor;
    this.dislikeList = this.$utils.dislike;
    await this.getUserInfo();
    this.getBookInfo();
    this.getFoodList();
    this.getCommitList();
    this.isFollow();
  },
  methods: {
    currStyle(img) {
      return `background-image:url(${img});width:150px;height:100px;`;
    },
    getCurrStyle() {
      return `background-image:url(${
        this.image_url
      });background-size: cover;width:100%;height:200px;background-color:#eee;background-size: cover;`;
    },
    async isFollow() {
      const { data } = await this.$http({
        url: this.API.CHECK_FOLLOW,
        method: "post",
        data: {
          fans: this.$store.state.users.id,
          star: this.user.id
        }
      });
      this.is_follow = data.is_follow;
    },
    async onFollow(type) {
      const { data } = await this.$http({
        url: this.API.FOLLOW,
        method: "post",
        data: {
          fans: this.$store.state.users.id,
          star: this.user.id,
          handle: type ? "remove" : "follow"
        }
      });
      this.$Message.success((type ? "remove" : "follow") + "  successful");
      await this.getUserInfo();
      this.isFollow();
    },
    async getCommitList() {
      const { data } = await this.$http({
        url: this.API.COMMIT_ADD,
        params: {
          auther: this.$route.query.userId
        }
      });
      let score = 0;
      data.map(item => {
        score += item.score;
      });
      this.score = score / data.length;
      this.commitList = data;
    },
    async getUserInfo() {
      const { data } = await this.$http({
        url: this.API.UPDATE_USER(this.$route.query.userId),
        method: "get"
      });
      this.user = data;
      this.image_url = data.image_url;
      this.last_name = data.last_name
    },
    async onFileSuccess(res) {
      await this.$http({
        url: this.API.UPDATE_USER(this.$route.query.userId),
        method: "PATCH",
        data: {
          image_url: res.url
        }
      });
      this.getUserInfo();
    },
    async getFoodList() {
      const { data } = await this.$http({
        url: this.API.FOOD_LIST,
        params: {
          auther: this.$route.query.userId
        }
      });
      this.foodList = data.sort((a, b) => {
        if (a.date > b.date) {
          return -1;
        } else {
          return 1;
        }
      });
      this.foodList = this.foodList.filter(item => {
        return +new Date() >= item.date;
      });
    },
    async getBookInfo() {
      const { data } = await this.$http({
        url: this.API.BOOK_LIST_Q(this.$route.query.userId)
      });
      this.bookList = data.map(item => {
        if (item.food_detail) {
          item.food_detail = JSON.parse(item.food_detail);
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
    },
    async onCommitAdd() {
      await this.$http({
        url: this.API.COMMIT_ADD,
        method: "post",
        data: {
          description: this.modal.content,
          score: this.modal.score,
          auther: this.$route.query.userId,
          food: this.modal.id
        }
      });
      this.isCommit = false;
      //刷新列表
      this.getBookInfo();
      this.$Message.success("Evaluation success!");
    }
  }
};
</script>

<style lang="less">
@import "./style.less";
</style>
