<template>
  <div class="post">
    <div class="post-header">
      <div class="post-left" @click="$router.push({name:'Home'})">
        <img src="@/resource/fanhui.svg" alt="">
      </div>
      <span>Foodish</span>
    </div>
    <div class="post-main">
      <Form class="post-main-form" :label-width="100" ref="form" :model="forms" :rules="rules">
        <div class="post-main-left">
          <FormItem prop="image_url" :label-width="0">
            <Upload :on-success="onFileSuccess" name="img" :show-upload-list="false" multiple type="drag" :action="API.IMAGE_UPLOAD">
              <div v-if="!forms.image_url" style="padding: 120px 0">
                <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
              </div>
              <div v-else :style="`background:url(${forms.image_url}) no-repeat top center;
                background-size: cover;width:100%;height:300px`">
              </div>
            </Upload>
          </FormItem>
        </div>
        <div class="post-main-right">
          <FormItem label="Food name" prop="name">
            <Input type="text" v-model="forms.name" placeholder="" style="width:450px"></Input>
          </FormItem>
          <FormItem label="Price" prop="price">
            <InputNumber v-model="forms.price" :max="10000" :min="1" style="width:450px"></InputNumber>
          </FormItem>
          <FormItem label="Date" prop="date">
            <DatePicker :options="options" v-model="forms.date" type="datetime" style="width:450px"></DatePicker>
          </FormItem>
          <FormItem label="Place" prop="place">
            <Input type="text" v-model="forms.place" style="width:450px"></Input>
          </FormItem>
          <FormItem label="People" prop="max_book">
            <InputNumber :max="10000" v-model="forms.max_book" :min="1" style="width:450px"></InputNumber>
          </FormItem>
        </div>
        <div class="post-main-desc">
          <FormItem label="Desc" prop="content">
            <Input type="textarea" v-model="forms.content" :rows="4"></Input>
          </FormItem>
          <FormItem label="Flavor" prop="flavor">
            <Tag @click.native="onTagSelect('flavor',item.val)" :color="getIsActive('flavor',item.val,flavorList)" v-for="item in flavorList" :key="item.val">{{item.text}}</Tag>
          </FormItem>
          <FormItem label="Pay attention" prop="dislike">
            <Tag @click.native="onTagSelect('dislike',item.val)" :color="getIsActive('dislike',item.val,dislikeList)" v-for="item in dislikeList" :key="item.val">{{item.text}}</Tag>
          </FormItem>
          <FormItem>
            <Button @click="submit" long size="large" type="warning">Submit</Button>
          </FormItem>
        </div>
      </Form>
    </div>
    <div class="text-modal" v-if="isShow">
      <span style="color:#f95;font-size:100px">Weell Done!</span>
    </div>
  </div>
</template>

<script>
import * as Rules from "@/utils/validate";
export default {
  data() {
    return {
      isShow: false,
      forms: {
        image_url: "",
        name: "", //菜品名字
        price: 0, //价格
        place: "",
        date: "",
        max_book: 0, //最大预定数量
        content: "", //简介
        book_now: "", //当前预定数量
        diet: "", //忌口类型
        style: "", //菜品口味类型
        author: "" //创建的作者
      },
      flavor: [],
      dislike: [],
      rules: {
        image_url: Rules.required("the is required"),
        name: Rules.required("the is required"),
        price: Rules.number("the is required", {
          min: 1
        }),
        place: Rules.required("the is required"),
        date: {
          type: "date",
          required: true,
          message: "the is required",
          trigger: "change"
        },
        max_book: Rules.number("the is required", {
          min: 1
        }),
        content: Rules.required("the is required")
      },
      flavorList: [],
      dislikeList: [],
      options: {
        disabledDate(date) {
          return (
            date && date.valueOf() <= new Date().valueOf() + 24 * 60 * 60 * 1000
          );
        }
      }
    };
  },
  created() {
    this.flavorList = this.$utils.flavor;
    this.dislikeList = this.$utils.dislike;
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
    async submit() {
      const result = await this.$refs.form.validate();
      if (!result) return;
      try {
        const { data } = await this.$http({
          url: this.API.FOOD,
          method: "post",
          data: this.getParams()
        });
        this.isShow = true;
        setTimeout(() => {
          this.$router.replace({ name: "Home" });
        }, 2000);
      } catch (error) {
        this.$Message.error("error");
      }
    },
    async onFileSuccess(res) {
      this.forms.image_url = res.url;
    },
    getParams() {
      let author = "";
      try {
        author = this.$store.state.users.id;
      } catch (error) {}
      return {
        ...this.forms,
        book_now: 0,
        date: +new Date(this.forms.date),
        price: this.forms.price * 100,
        diet: this.dislike.join(","),
        style: this.flavor.join(","),
        author
      };
    }
  }
};
</script>

<style lang="less">
@import "./style.less";
.text-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "PingFang SC";
}
</style>
