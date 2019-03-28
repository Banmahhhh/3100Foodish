<template>
  <div :style="`${commit?'height:230px':''}`" class="food-item" :class="align==='right'?'food-item-align-right':''">
    <div class="foo-item-image" >
        <div :style="currStyle(item.image_url)" @click="$router.push({name:'Info',query:{id:item.id,userName:item.auther_name}})">

        </div>
    </div>
    <div class="foo-item-main" :class="align==='right'?'food-item-main-right':''">
      <h3>{{item.name}}</h3>
      <Progress :percent="(item.book_now/item.max_book)*100" status="active">
        {{item.book_now}}/{{item.max_book}}
      </Progress>
      <div class="item-main-row">
        <label>Price
          <i></i>
        </label>
        <span class="text-ellipsis">：
          <i style="color:#f95;font-size:22px;">$ {{item.price | money}}</i>
        </span>
      </div>
      <div class="item-main-row">
        <label>Score
          <i></i>
        </label>
        <span class="text-ellipsis">：
          <Rate :value="item.score" disabled />
        </span>
      </div>
      <div class="item-main-row">
        <label>Picking time
          <i></i>
        </label>
        <span class="text-ellipsis">：{{item.date | dateFormat('yyyy-MM-dd hh:mm')}}</span>
      </div>
      <div class="item-main-row">
        <label>Picking place
          <i></i>
        </label>
        <span class="text-ellipsis">：{{item.place}}</span>
      </div>
      <div v-if="commit&&!isCommit" class="item-main-row" style="padding-top:8px">
        <Button type="warning" @click="$emit('evaluate',item)">To evaluate</Button>
      </div>
      <div v-if="comming" class="item-main-row" style="padding-top:0">
        <p :style="item.orderStatus===0?'color:#f95':'color:rgb(51, 153, 255)'">{{item.orderText}}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    infoBtn:{
      type:Boolean,
      default:true
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
    },
    comming:{
      type:Boolean,
      default:false
    },
    commit:{
      type:Boolean,
      default:false
    },
    isCommit:{
      type:Boolean,
      default:false
    }
  },
  methods:{
    currStyle(img) {
      return `background:url(${img}) no-repeat center center;background-size: cover;width:150px;height:150px`;
    },
  }
};
</script>

<style lang="less" scoped>
.food-item {
  display: flex;
  align-items: center;
  min-height:200px;
  height:auto;
  border-bottom: 1px solid #e0e0e0;
  padding: 0;
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
  padding: 10px 0;
  padding-left: 30px;
  h3 {
    font-size: 14px;
    padding-bottom: 10px;
  }
  .item-main-row {
    color: #323232;
    font-size: 12px;
    line-height: 25px;
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
  padding-right: 30px;
  padding-left: 0;
}
.foo-item-image {
  width: 150px;
  overflow: hidden;
  height: 100%;
  display: flex;
    align-items: center;
}
.foo-item-image img {
  width: 100%;
  background-color: #f0f0f0;
  height: 100px;
  display: block;
}
.foo-item-image p {
  font-size: 14px;
  color: #323232;
  line-height: 40px;
}
</style>
