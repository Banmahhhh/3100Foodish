<template>
  <div ref="page" class="login" @click="onPageClick">
    <Carousel loop autoplay :autoplay-speed="5000" arrow="never">
      <CarouselItem v-for="(img, index) in data" :key="index">
        <div class="carousel" :style="currStyle(img)"></div>
      </CarouselItem>
    </Carousel>
    <div class="logo-wrap" :style="hide ? 'top:50%' : 'top:35%'">
      <div
        @click="hide = false"
        class="logo"
        :style="currStyle(require('@/resource/logo.jpg'))"
      ></div>
      <h3>Foodish</h3>
      <Form
        class="form-hide"
        :style="hide ? 'opacity:0' : 'opacity:1'"
        ref="form"
        :model="forms"
        :rules="rules"
        @click.stop="() => {}"
      >
        <FormItem v-if="status == 1" prop="name">
          <Input
            class="login-input"
            size="large"
            v-model="forms.name"
            placeholder="Enter your name"
          ></Input>
        </FormItem>
        <FormItem prop="email">
          <Input
            class="login-input"
            size="large"
            v-model="forms.username"
            placeholder="Enter your email"
          ></Input>
        </FormItem>
        <FormItem prop="password">
          <Input
            type="password"
            class="login-input"
            size="large"
            v-model="forms.password"
            placeholder="Enter your password"
          ></Input>
        </FormItem>
        <FormItem v-if="status == 1" prop="password2">
          <Input
            type="password"
            class="login-input"
            size="large"
            v-model="forms.password2"
            placeholder="Enter your password"
          ></Input>
        </FormItem>
        <div class="form-footer">
          <Button size="large" @click="login">login</Button>
          <Button size="large" @click="signup">signup</Button>
        </div>
      </Form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      status: 0, //0是登录 1是注册
      hide: true, //是否显示
      forms: {
        name: "",
        username: "",
        password: "",
        password2: ""
      },
      data: [
        require("@/resource/3.jpg"),
        require("@/resource/4.jpg"),
        require("@/resource/5.jpg"),
        require("@/resource/6.jpg"),
        require("@/resource/7.jpg")
      ]
    };
  },
  computed: {
    rules() {
      //This username has been used
      //Invalid username or password
      if (!this.status) {
        return {
          username: {
            required: true,
            message: "User name cannot be empty",
            trigger: "blur"
          },
          password: {
            required: true,
            message: "Password cannot be empty",
            trigger: "blur"
          }
        };
      } else {
        return {
          name: {
            required: true,
            message: "User name cannot be empty",
            trigger: "blur"
          },
          username: {
            required: true,
            message: "User username cannot be empty",
            trigger: "blur"
          },
          password: {
            required: true,
            message: "Password cannot be empty",
            trigger: "blur"
          },
          password2: {
            required: true,
            message: "Password cannot be empty",
            trigger: "blur"
          }
        };
      }
    }
  },
  methods: {
    currStyle(img) {
      return `background:url(${img}) no-repeat center center;background-size: cover;`;
    },
    onPageClick(e) {
      const { pageX, pageY } = e;
      const img = document.createElement("img");
      img.src = require("@/resource/aixin.svg");
      img.className = "login-aixin aixin-animation";
      img.style.left = pageX - 15 + "px";
      img.style.top = pageY - 15 + "px";
      this.$refs.page.appendChild(img);
      setTimeout(() => {
        this.$refs.page && this.$refs.page.removeChild(img);
      }, 1000);
    },
    async login() {
      if (this.status == 1) {
        this.status = 0;
        return;
      }
      const result = await this.$refs.form.validate();
      if (!result) return;
      try {
        const { data } = await this.$http({
          url: this.API.LOGIN,
          method: "post",
          data: this.forms
        });
        const { token } = data;
        this.$store.commit("users", { token });
        const { data: list } = await this.$http({
          url: this.API.USER_LIST(this.forms.username)
        });
        this.$store.commit("users", { token, ...list[0] });
        this.$Message.success("login successfully");
        this.$router.replace({
          name: "Home"
        });
      } catch (error) {
        this.$Message.error("Invalid username or password");
      }
    },
    async signup() {
      if (this.status == 0) {
        this.status = 1;
        return;
      }
      const result = await this.$refs.form.validate();
      if (!result) return;
      if (this.forms.password !== this.forms.password2) {
        this.$Message.error("The two passwords are inconsistent!");
        return;
      }
      if (this.forms.username.indexOf("@") == -1) {
        this.$Message.error("The mailbox format is incorrect");
        return;
      }
      try {
        const { data } = await this.$http({
          url: this.API.REGISTER,
          method: "post",
          data: this.forms
        });
        this.$Message.success("signup was successful");
      } catch (error) {
        this.$Message.error("This username has been used");
      }
    }
  }
};
</script>

<style lang="less" scoped>
.login {
  width: 100%;
  height: 100%;
  position: relative;
  .ivu-carousel {
    height: 100%;
  }
}
.login /deep/ .ivu-carousel-track,
.login /deep/ .ivu-carousel-list,
.login /deep/ .ivu-carousel-item,
.login /deep/ .carousel {
  height: 100% !important;
}
.login /deep/ .ivu-input {
  background-color: transparent;
  border-color: #fff;
  border-radius: 100px;
  width: 300px;
  color: #fff;
}
.login /deep/ input {
  padding-left: 20px;
}
.login /deep/ .ivu-form-item-error-tip {
  padding-left: 20px;
}
.login /deep/ .ivu-input:focus {
  border-color: #fff;
  box-shadow: 0 0 0 transparent;
}
.login /deep/ input::-webkit-input-placeholder {
  /* WebKit browsers */
  color: #fff;
}
.login /deep/ input:-moz-placeholder {
  /* Mozilla Firefox 4 to 18 */
  color: #fff;
}
.login /deep/ input::-moz-placeholder {
  /* Mozilla Firefox 19+ */
  color: #fff;
}
.login /deep/ input:-ms-input-placeholder {
  /* Internet Explorer 10+ */
  color: #fff;
}
.form-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.form-footer /deep/ .ivu-btn {
  background-color: transparent;
  border-radius: 100px;
  color: #fff;
  width: 140px;
  border-color: #fff;
  background-color: transparent;
}
.logo-wrap {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  transition: top 1.2s;
  .logo {
    width: 80px;
    height: 80px;
    border-radius: 150px;
    border: 1px solid #fff;
    cursor: pointer;
    margin: 0 auto;
  }
  h3 {
    color: #fff;
    text-align: center;
    font-size: 48px;
    font-family: Georgia, serif;
  }
}
</style>
<style>
.login-aixin {
  position: absolute;
  width: 30px;
  height: 30px;
  z-index: 9;
}
.aixin-animation {
  animation: aixin 1s forwards;
}
@keyframes aixin {
  0% {
    opacity: 0.95;
    transform: translateY(0);
  }
  50% {
    opacity: 0.9;
  }
  100% {
    opacity: 0;
    transform: translateY(-100px);
  }
}
.form-hide {
  opacity: 0;
  transition: opacity 1.2s;
}
</style>
