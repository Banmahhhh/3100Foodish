<template>
  <div class="info">
    <div class="info-header">
      <div class="info-left" @click="$router.back()">
        <img src="@/resource/fanhui.svg" alt="">
      </div>
      <span>Foodish</span>
    </div>
    <div class="info-main">
      <FoodItem :item="item" :infoBtn="false" />
      <div class="item-main-row">
        <label>Flavor
          <i></i>
        </label>
        <span class="text-ellipsis">：{{item.flavor}}</span>
      </div>
      <div class="item-main-row">
        <label>Dislike
          <i></i>
        </label>
        <span class="text-ellipsis">：{{item.dislike}}</span>
      </div>
      <div class="item-footer">
        <Button @click="onDelete(item)" v-if="isPerson" size="large" type="warning">cancel it</Button>
        <Button @click="onReserve(item.id)" v-else-if="!isPerson&&!isBooked" size="large" type="warning">reserve it</Button>
        <Button @click="onDeleteReserve(item.id)" v-else-if="!isPerson&&isBooked" size="large" type="warning">cancel it</Button>
      </div>
      <!-- 评论 -->
      <div class="commit">
        <CommitItem v-for="item in commitList" :key="item.id" :item="item" />
      </div>
    </div>
  </div>
</template>

<script>
import FoodItem from "@/components/FoodItem";
import CommitItem from "@/components/CommitItem";
export default {
  components: { FoodItem, CommitItem },
  data() {
    return {
      userid: "",
      item: {},
      forms: {},
      rules: {},
      flavorList: [],
      dislikeList: [],
      bookList: [],
      commitList: [],
      userName:""
    };
  },
  computed: {
    isPerson() {
      return this.item.author === this.$store.state.users.id;
    },
    isBooked() {
      const result = this.bookList.find(item => {
        return item.food === this.item.id;
      });
      return result ? true : false;
    }
  },
  async created() {
    this.flavorList = this.$utils.flavor;
    this.dislikeList = this.$utils.dislike;
    await this.getInfo();
    this.getBookInfo();
    this.getCommitList();
  },
  methods: {
    async getCommitList() {
      const { id } = this.$route.query;
      const { data } = await this.$http({
        url: this.API.COMMIT_ADD,
        params: {
          food: id
        }
      });
      this.commitList = data;
    },
    async getBookInfo() {
      const { data } = await this.$http({
        url: this.API.BOOK_LIST_Q(this.$store.state.users.id)
      });
      this.bookList = data;
    },
    async onDelete({ id, content }) {
      const currDate = +new Date();
      if (this.item.date - currDate < 24 * 60 * 60 * 1000) {
        this.$Modal.error({
          title: "Tips",
          content: "Sorry , you cannot cancel it now!"
        });
        return;
      }
      await this.$http({
        url: this.API.FOOD_UPDATE(id),
        method: "put",
        data: {
          content,
          is_cancel: true
        }
      });
      this.$Message.success("You have cancel it successfull!");
      this.$router.replace({ name: "Home" });
    },
    //取消预订
    async onDeleteReserve(id) {
      const currDate = +new Date();
      if (this.item.date - currDate < 24 * 60 * 60 * 1000) {
        this.$Modal.error({
          title: "Tips",
          content: "Sorry , you cannot cancel it now!"
        });
        return;
      }
      await this.$http({
        url: this.API.BOOK_DEL(this.bookList[0].id),
        method: "delete"
      });
      await this.getBookInfo();
      this.getInfo();
      this.$Modal.success({
        title: "Tips",
        content: "You have cancel it successfull!"
      });
    },
    async onReserve(id) {
      const currDate = +new Date();
      if (this.item.date - currDate < 24 * 60 * 60 * 1000) {
        this.$Modal.error({
          title: "Tips",
          content: "Sorry , you cannot reserve it now!"
        });
        return;
      }
      await this.getInfo();
      if (this.item.book_now === this.item.max_book) {
        this.$Modal.success({
          title: "Tips",
          content: "Sorry , You cannot reserve it now!"
        });
        return;
      }
      await this.$http({
        url: this.API.BOOK,
        method: "post",
        data: { food: id, user: this.$store.state.users.id }
      });
      await this.getBookInfo();
      this.getInfo();
      this.$Modal.success({
        title: "Tips",
        content: "You have reserved it successfull!"
      });
    },
    async getInfo() {
      const { id } = this.$route.query;
      const { data } = await this.$http({
        url: this.API.FOOD_INFO(id)
      });
      let result = data || {};
      result.style += "";
      result.diet += "";
      let flavor = result.style.split(",");
      let dislike = result.diet.split(",");
      flavor = flavor
        .map(item => {
          let val = +item;
          let flavorItem = this.flavorList.find(m => {
            return m.val === val;
          });
          return flavorItem ? flavorItem.text : "";
        })
        .join(" ");

      dislike = dislike
        .map(item => {
          let val = +item;
          let dislikeItem = this.dislikeList.find(m => {
            return m.val === val;
          });
          return dislikeItem ? dislikeItem.text : "";
        })
        .join(" ");
      this.item = {
        ...result,
        dislike,
        flavor,
        auther_name :this.$route.query.userName
      };
      console.log(this.item)
    }
  }
};
</script>

<style lang="less">
@import "./style.less";
</style>
