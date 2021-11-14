<template>
  <div>
    <el-input
      v-model='email'
      :prefix-icon='userIcon'
    />
    <el-input
      v-model='email'
      :prefix-icon='pwdIcon'
    />
    <el-button>Login</el-button>
  </div>
</template>

<script>
  import { User, Lock } from '@element-plus/icons';
  import { ElInput, ELButton } from 'element-plus';

  import { ref } from 'vue';

  export default {
    components: {
      ElInput,
      ELButton,
    },
    setup() {
      return {
        email: ref(''),
        userIcon: User,
        pwdIcon: Lock,
      };
    },
  };
</script>