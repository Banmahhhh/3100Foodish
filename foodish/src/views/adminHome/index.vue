<template>
  <div class="person">
    <div class="person-header">
      <span>Foodish</span> <span>{{ $store.state.users.name }}</span>
      <Avatar
        :src="$store.state.users.image_url"
        icon="ios-person"
        size="large"
        @click.native="loginout"
      />
    </div>
    <div class="person-main-form">
      <FoodItem
        v-for="item in foodList"
        :key="item.id"
        :item="item.food"
        :infoBtn="item.user_detail.isStop"
      />
    </div>
  </div>
</template>

<script>
import FoodItem from "@/components/FoodItemAdmin";
export default {
  components: { FoodItem },
  data() {
    return {
      active: 0,
      commitId: "",
      isCommit: false,
      image_url: "",
      last_name: "",
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
    uname() {
      return this.user.name;
    },
    username() {
      return this.user.username;
    }
  },
  async created() {
    await this.getUserInfo();
    this.getList();
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
    async getUserInfo() {
      const { data } = await this.$http({
        url: this.API.UPDATE_USER(this.$store.state.users.id),
        method: "get"
      });
      this.user = data;
      this.image_url = data.image_url;
      this.last_name = data.last_name;
    },

    async getList() {
      const { data } = await this.$http({
        url: this.API.COMPLAIN
      });
      let list = [];
      data.map(item => {
        if (item.user_detail) {
          item.user_detail = JSON.parse(item.user_detail);
        }
        list.push(item.food);
      });
      list = [...new Set(list)];
      list = list.map(item => {
        return this.$http({
          url: this.API.FOOD_INFO(item)
        });
      });
      const result = await Promise.all(list);
      const map = {};
      result.map(({ data }) => {
        map[data.id] = data;
        return data;
      });
      this.foodList = data.map(item => {
        item.food = map[item.food];
        return item;
      });
    },
    loginout() {
      this.$Modal.confirm({
        title: "Tips",
        content: "Whether to log out or not?",
        onOk: () => {
          this.$store.commit("users", {});
          this.$router.replace({ name: "Login" });
        }
      });
    }
  }
};
</script>

<style lang="less">
@import "./style.less";
</style>
<style lang="less" scoped>
.person-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
