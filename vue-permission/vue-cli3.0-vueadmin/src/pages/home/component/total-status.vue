<template>
  <div class="demo-image__placeholder">
    <div class="block">
      <el-image :src="src">
      <div slot="placeholder" class="image-slot">
        加载中<span class="dot">...</span>
      </div>
    </el-image>
    </div>
  </div>
</template>

<script>
export default {
    data() {
        return {
            src:
                'https://gitee.com/my_netinlove/Picturebed/raw/master/images/1595292629962.jpg'
        }
    }
}
</script>
