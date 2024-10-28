<template>
  <div>
    <el-button v-if="!showDrawer" @click="onButtonClick" plain circle class="fix-bottom-right">
      <el-icon size="25">
        <chat-dot-square />
      </el-icon>
    </el-button>

    <el-drawer v-model="showDrawer" direction="rtl" :lock-scroll="false">
      <template #header>
        <h4 style="margin-bottom: 0px;">想询问关于{{ page }}的什么</h4>
      </template>
      <template #default>
        <table style="border-collapse: separate; border-spacing: 10px 20px; margin-top: -35px;">
          <tbody>
            <tr v-for="chat in chats" :key="chat">
              <td valign="top">
                <el-avatar style="width: 40px">
                  <el-icon size="20">
                    <opportunity v-if="chat.role === 'assistant'" />
                    <user-filled v-else />
                  </el-icon>
                </el-avatar>
              </td>
              <td style="text-align: left;">
                <div :style="`background-color: ${chat.role === 'assistant' ? '#f3f4f6' : '#d2e3fd'};`" class="dialog">
                  {{ chat.content }}
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </template>
      <template #footer>
        <el-input v-model="query" style="max-width: 100%; margin-top: 5px; margin-bottom: 5px;"
          placeholder="Press enter to send">
        </el-input>
      </template>
    </el-drawer>
  </div>
</template>

<script>
import { ChatDotSquare, UserFilled, Opportunity } from '@element-plus/icons-vue';
export default {
  name: 'SideChat',
  props: {
    page: String
  },
  data () {
    return {
      showDrawer: false,
      query: '',
      chats: [
        {
          role: 'user',
          content: 'Hello, I have a question about this page, Hello, I have a question about this page, Hello, I have a question about this page'
        },
        {
          role: 'assistant',
          content: 'Sure, what do you want to know?'
        },
        {
          role: 'user',
          content: 'I want to know more about this page'
        },
        {
          role: 'assistant',
          content: 'I can help you with that'
        },
        {
          role: 'user',
          content: 'Thank you'
        },
        {
          role: 'assistant',
          content: 'You are welcome'
        },
        {
          role: 'user',
          content: 'Hello, I have a question about this pageHello, I have a question about this page Hello, I have a question about this page Hello, I have a question about this page Hello, I have a question about this page'
        },
        {
          role: 'assistant',
          content: 'Sure, what do you want to know?'
        },
        {
          role: 'user',
          content: 'I want to know more about this page'
        },
        {
          role: 'assistant',
          content: 'I can help you with that'
        },
        {
          role: 'user',
          content: 'Thank you'
        },
        {
          role: 'assistant',
          content: 'You are welcome'
        },
      ],

      onButtonClick: () => {
        this.showDrawer = !this.showDrawer;
        console.log(this.page);
      }
    }
  },
  components: {
    ChatDotSquare,
    UserFilled,
    Opportunity
  },
}
</script>

<style scoped>
.fix-bottom-right {
  position: fixed;
  bottom: 30px;
  right: 20px;
  width: 50px;
  height: 50px;
}

.dialog {
  border-radius: 10px;
  border-top-left-radius: 0px;
  padding: 8px;
  width: fit-content;
}
</style>