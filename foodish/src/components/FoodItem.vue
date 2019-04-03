<template>
  <div
    class="food-item"
    :class="align === 'right' ? 'food-item-align-right' : ''"
  >
    <div class="foo-item-image">
      <img
        :src="item.food_image_url"
        alt=""
        @click="$router.push({ name: 'Info', query: { id: item.id } })"
      />
      <p @click="toInfo(item)" class="food-col-p-center">
        {{ item.nickname || "" }}
      </p>
      <Progress
        :percent="(item.book_now / item.max_book) * 100"
        status="active"
      >
        {{ item.book_now }}/{{ item.max_book }}
      </Progress>
    </div>
    <div
      class="foo-item-main"
      :class="align === 'right' ? 'food-item-main-right' : ''"
    >
      <h3>{{ item.name }}</h3>
      <div class="item-main-row">
        <label>Price <i></i> </label>
        <span class="text-ellipsis"
          >：
          <i style="color:#f95;font-size:22px;">$ {{ item.price | money }}</i>
        </span>
      </div>
      <div class="item-main-row">
        <label>Score <i></i> </label>
        <span class="text-ellipsis"
          >：
          <Rate :value="item.score" disabled />
        </span>
      </div>
      <div class="item-main-row">
        <label>Picking time <i></i> </label>
        <span class="text-ellipsis"
          >：{{ item.date | dateFormat("yyyy-MM-dd hh:mm") }}</span
        >
      </div>
      <div class="item-main-row">
        <label>Picking place <i></i> </label>
        <span class="text-ellipsis">：{{ item.place }}</span>
      </div>
      <div class="item-main-row">
        <label>Introduction <i></i> </label>
        <span class="text-ellipsis">：{{ item.content }}</span>
      </div>
      <div v-if="infoBtn" class="item-main-row" style="padding-top:8px">
        <Button
          type="warning"
          @click="$router.push({ name: 'Info', query: { id: item.id } })"
          >View details</Button
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    infoBtn: {
      type: Boolean,
      default: true
    },
    align: {
      type: String,
      default: "left"
    },
    item: {
      type: Object,
      default() {
        return {};
      }
    }
  },
  methods: {
    toInfo(item) {
      if (item.author != this.$store.state.users.id) {
        this.$router.push({
          name: "PersonHome",
          query: { userId: item.author }
        });
      }
    }
  }
};
</script>

<style lang="less">
.food-item {
  display: flex;
  align-items: center;
  padding: 30px 50px;
  height: 320px;
  border-bottom: 1px solid #e0e0e0;
  .ivu-btn-warning,
  .ivu-progress-bg {
    background-color: #f95;
    border-radius: 100px;
  }
  .ivu-rate-star-full:before,
  .ivu-rate-star-half .ivu-rate-star-content:before {
    color: #f95;
  }
}
.food-item-align-right {
  flex-direction: row-reverse;
}
.foo-item-main {
  flex: 1;
  overflow: hidden;
  height: 100%;
  padding-left: 50px;
  h3 {
    font-size: 16px;
    padding-bottom: 30px;
  }
  .item-main-row {
    color: #323232;
    font-size: 14px;
    line-height: 30px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    label {
      width: 6em;
      text-align: justify;
      height: 30px;
      i {
        display: inline-block;
        width: 100%;
        line-height: 0;
      }
    }
    span {
      flex: 1;
    }
  }
}
.food-item-main-right {
  padding-right: 50px;
  padding-left: 0;
}
.foo-item-image {
  width: 300px;
  overflow: hidden;
}
.foo-item-image img {
  width: 100%;
  background-color: #f0f0f0;
  height: 200px;
  display: block;
}
.foo-item-image p {
  font-size: 14px;
  color: #323232;

  line-height: 40px;
}
.food-item {
  .food-col-p-center {
    display: flex;
    align-items: center;
    padding: 5px 0;
    img {
      width: 40px;
      height: 40px;
      border-radius: 50px;
      background-color: #f5f5f5;
      border: 1px solid #f5f5f5;
      margin-right: 5px;
      overflow: hidden;
    }
  }
}
</style>
