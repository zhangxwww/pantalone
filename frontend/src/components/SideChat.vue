<template>
  <div>
    <el-button v-if="!showDrawer" @click="onButtonClick" plain circle class="fix-bottom-right">
      <el-icon size="25">
        <chat-dot-square />
      </el-icon>
    </el-button>

    <el-drawer v-model="showDrawer" @opened="onDrawerOpen" direction="rtl" :lock-scroll="false">
      <template #header>
        <h4 style="margin-bottom: 0px;">想询问关于{{ page }}的什么</h4>
      </template>
      <template #default>
        <el-scrollbar ref="scrollbarRef" style="">
          <table style="border-collapse: separate; border-spacing: 10px 20px;">
            <tbody>
              <tr v-for="chat in chats" :key="chat">
                <td valign="top">
                  <el-avatar style="width: 40px">
                    <el-icon size="20">
                      <opportunity v-if="chat.role === 'ai'" />
                      <user-filled v-else />
                    </el-icon>
                  </el-avatar>
                </td>
                <td style="text-align: left;">
                  <div v-if="chat.role === 'ai'" style="background-color: #f3f4f6;" class="dialog">
                    <v-md-editor v-model="chat.content" mode="preview" />
                  </div>
                  <div v-else style="background-color: #d2e3fd;" class="dialog">
                    {{ chat.content }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </el-scrollbar>
      </template>
      <template #footer>
        <el-input v-model="query" @keyup.enter="sendMessage"
          style="max-width: 100%; margin-top: 5px; margin-bottom: 5px;" placeholder="Press enter to send">
        </el-input>
      </template>
    </el-drawer>
  </div>
</template>

<script>
import { ChatDotSquare, UserFilled, Opportunity } from '@element-plus/icons-vue';
import { chatStreamRequest } from '../scripts/requests';

export default {
  name: 'SideChat',
  props: {
    page: String
  },
  data () {
    return {
      showDrawer: false,
      query: '',
      streaming: false,
      chats: [],

      scrollToBottom: () => {
        this.$nextTick(() => {
          this.$refs.scrollbarRef.setScrollTop(100000);
        });
      },

      onButtonClick: () => {
        this.showDrawer = !this.showDrawer;
      },

      onDrawerOpen: () => {
        this.scrollToBottom();
      },

      sendMessage: async () => {
        if (this.query && !this.streaming) {
          this.chats.push({
            role: 'user',
            content: this.query
          }, {
            role: 'ai',
            content: ''
          });
          this.streaming = true;
          this.scrollToBottom();
          this.query = '';
          await chatStreamRequest({
            'messages': this.chats,
            'page': this.page
          }, (chunk) => {
            if (chunk.length > 1 && chunk.endsWith('\n')) {
              chunk = chunk.slice(0, -1);
            }
            this.chats[this.chats.length - 1].content += chunk;
            this.scrollToBottom();
          }, () => {
            this.streaming = false;
          });
        }
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

<style>
.vuepress-markdown-body:not(.custom) {
  padding: 5px 5px;
  background-color: #f3f4f6;
}

.vuepress-markdown-body {
  max-width: 350px;
}

.el-drawer__header {
  align-items: center;
  color: #72767b;
  display: flex;
  margin-bottom: 15px;
  padding: var(--el-drawer-padding-primary);
  padding-bottom: 0;
}

.el-drawer__body {
  flex: 1;
  overflow: auto;
  padding: 0px;
}
</style>