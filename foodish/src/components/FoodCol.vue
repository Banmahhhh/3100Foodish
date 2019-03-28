<template>
  <div class="food-col">
    <div>
      <img
        style="width:100%"
        :src="item.image_url"
        alt=""
        @click="$router.push({ name: 'Info', query: { id: item.id } })"
      />
    </div>
    <div class="food-col-main">
      <h3>{{ item.name }}</h3>
      <p class="text-ellipsis">
        <i style="color:#f95;">$ {{ item.price | money }}</i>
      </p>
      <Rate :value="item.score" disabled />
      <div class="item-main-row">
        <label
          >Picking time
          <i></i>
        </label>
        <span class="text-ellipsis"
          >：{{ item.date | dateFormat("yyyy-MM-dd hh:mm") }}</span
        >
      </div>
      <div class="item-main-row">
        <label
          >Picking place
          <i></i>
        </label>
        <span class="text-ellipsis">：{{ item.place }}</span>
      </div>
      <Progress :percent="(item.book_now/item.max_book)*100" status="active">
        {{ item.book_now }}/{{ item.max_book }}
      </Progress>
      <div v-if="infoBtn" style="padding-top:8px;text-align:center">
        <Button
          type="warning"
          size="small"
          @click="
            $router.push({
              name: 'Info',
              query: { id: item.id, userName: item.auther_name }
            })
          "
          >View details</Button
        >
      </div>
    </div>
    <div class="food-col-footer">
      <p class="food-col-p-center">
        {{ item.nickname || "" }}
      </p>
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
    item: {
      type: Object,
      default() {
        return {};
      }
    }
  }
};
</script>

<style lang="less">
.food-col-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  line-height: 33px;
  padding: 0 15px 10px 15px;
}
.food-col-main {
  padding: 0 10px;
}
.food-col {
  display: block;
  background-color: #fff;
  margin: 0 0 30px 0;
  -webkit-box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.1);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  text-decoration: none;
  cursor: pointer;
  position: relative;
  border: 1px solid #f0f0f0;
}
.food-col-main::before {
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  content: " ";
  z-index: -1;
  background-color: rgba(0, 0, 0, 0.2);
  pointer-events: none;
}
.food-col:hover ::before {
  z-index: 1;
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
.food-col-p-center {
  display: flex;
  align-items: center;
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
</style>
