<template>
  <div class="home">
    <!-- headers -->
    <div class="home-header">
      <div class="home-add" @click="$router.push({name:'Post'})">
        <img src="@/resource/add.svg" alt="">
      </div>
      <div class="home-search" @mouseout="onSeachMouseout" @mouseover="onSeachMouseover">
        <Input clearable v-model="params.name" @on-enter="onSearchBox" @on-click="onSearchBox" @click.native="isSearch=true" prefix="ios-search" @on-focus="onSearchFocus" class="home-search-input" size="large" placeholder="" />
        <div v-show="isSearch" class="home-search-list">
          <Form :label-width="50">
            <FormItem label="flavor" style="margin-bottom:10px">
              <Tag @click.native="onTagSelect('flavor',item.val)" :color="getIsActive('flavor',item.val,flavorList)" v-for="item in flavorList" :key="item.val">{{item.text}}</Tag>
            </FormItem>
            <FormItem label="dislike" style="margin-bottom:10px">
              <Tag @click.native="onTagSelect('dislike',item.val)" :color="getIsActive('dislike',item.val,dislikeList)" v-for="item in dislikeList" :key="item.val">{{item.text}}</Tag>
            </FormItem>
          </Form>
        </div>
      </div>
      <div class="home-header-right">
        <Avatar :src="$store.state.users.image_url" @click.native="$router.push({name:'Person'})" icon="ios-person" size="large" />
        <span class="logo">Foodish</span>
      </div>
    </div>
    <!-- list -->
    <div class="home-list clearfix">
      <div class="home-col">
        <FoodCol v-if="index%4===0" v-for="(item,index) in list" :key="item.id" :item="item" />
      </div>
      <div class="home-col">
        <FoodCol v-if="index%4===1" v-for="(item,index) in list" :key="item.id" :item="item" />
      </div>
      <div class="home-col">
        <FoodCol v-if="index%4===2" v-for="(item,index) in list" :key="item.id" :item="item" />
      </div>
      <div class="home-col">
        <FoodCol v-if="index%4===3" v-for="(item,index) in list" :key="item.id" :item="item" />
      </div>
    </div>
  </div>
</template>

<script>
import FoodItem from "@/components/FoodItem";
import FoodCol from "@/components/FoodCol";
export default {
  components: { FoodItem, FoodCol },
  data() {
    return {
      isSearch: false,
      list: [],
      flavorList: [],
      dislikeList: [],
      flavor: [],
      dislike: [],
      params: {
        name: "",
        diet: "",
        style: ""
      }
    };
  },
  created() {
    this.getList();
    this.flavorList = this.$utils.ObjectParse(this.$utils.flavor);
    this.dislikeList = this.$utils.ObjectParse(this.$utils.dislike);
  },
  methods: {
    getIsActive(type, val, list) {
      const v = this[type].find(item => {
        return item === val;
      });
      return v ? "primary" : "blue";
    },
    onTagSelect(type, val) {
      const list = this[type];
      const v = list.find(item => {
        return item === val;
      });
      if (v) {
        this[type] = list.filter(item => {
          return item !== val;
        });
      } else {
        this[type].push(val);
      }
    },
    onSearchFocus() {
      this.isSearch = true;
    },
    onSeachMouseover() {
      this.timer && clearTimeout(this.timer);
    },
    onSearchBox() {
      this.params.diet = this.dislike.join(",");
      this.params.style = this.flavor.join(",");
      this.getList();
    },
    onSeachMouseout() {
      this.timer = setTimeout(() => {
        this.isSearch = false;
      }, 300);
    },
    async getList() {
      let params = { is_cancel: false };
      if (this.params.name) {
        params.name = this.params.name;
      }
      if (this.params.diet) {
        params.diet = this.params.diet;
      }
      if (this.params.style) {
        params.style = this.params.style;
      }
      const { data } = await this.$http({
        url: this.API.REMAD_LIST,
        method: "post",
        data: params
      });
      this.list = data || [];
      this.list = this.list.sort((a, b) => {
        if (a.date > b.date) {
          return -1;
        } else {
          return 1;
        }
      });
    }
  }
};
</script>

<style lang="less">
@import "./style.less";
</style>
