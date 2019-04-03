<template>
  <div class="commit-item">
    <div class="commit-item-row">
      <span class="commit-av-wrap" style="font-size:14px;color:#323232"
        ><img class="commit-av" :src="item.image_url" />{{
          user.name || user.nickname || user.username
        }}</span
      >
    </div>
    <div class="commit-item-row">
      <span style="font-size:12px;color:#999">{{
        item.created_time | dateFormat
      }}</span>
    </div>
    <div
      class="commit-item-row"
      style="padding:10px 0;font-size:14px;color:#323232"
    >
      {{ item.text }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    item: {
      type: Object,
      default() {
        return {};
      }
    },
    img: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      food: {},
      user: {}
    };
  },
  created() {
    try {
      this.user = JSON.parse(this.item.user_detail);
      console.log(this.user)
    } catch (error) {
      //
    }
    // this.getUserInfo();
  },
  methods: {
    async getUserInfo() {
      const { data } = await this.$http({
        url: this.API.USER_D_INFO(this.item.auther)
      });
      this.user = data;
    }
  }
};
</script>

<style lang="less">
.commit-item {
  border-bottom: 1px solid #ccc;
  .ivu-rate-star-full:before,
  .ivu-rate-star-half .ivu-rate-star-content:before {
    color: #f95;
  }
  .commit-item-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .commit-item-row .img {
    width: 150px;
    height: 100px;
    background-color: #ccc;
  }
}
.commit-av {
  width: 20px;
  height: 20px;
  border-radius: 50px;
  background-color: #f5f5f5;
  border: 1px solid #f5f5f5;
  margin-right: 5px;
  overflow: hidden;
}
.commit-av-wrap {
  display: flex;
  align-items: center;
}
</style>
