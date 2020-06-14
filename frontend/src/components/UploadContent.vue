<template>
  <div class="row">
    <div class="col-4">
      <div class="card">
        <div class="card-header">Texts</div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item" v-for="(text, index) in texts" :key="index">
            <a :href="text.id" @click.prevent="findSimilar(text.id)">{{ text.name }}</a>
          </li>
        </ul>
      </div>
    </div>
    <div class="col-8">
      <div class="card">
        <div class="card-header">Features</div>
        <div class="card-body">
          <h5 class="card-title">Text title</h5>
          <input
            type="text"
            placeholder="Please pass name here"
            v-model="text_title"
            id="text_title"
          />
          <br />
          <h5 class="card-title">Content</h5>
          <textarea spellcheck="true" placeholder="Please pass text here" v-model="text_content"></textarea>
          <button
            class="btn btn-success btn-block btn-primary"
            :disabled="!isTextInputsNotEmpty"
            @click="upload"
          >Upload</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-debugger */
import ApiService from "../services/ApiService";
import responseMixin from "../mixins/responseMixin";

export default {
  mixins: [responseMixin],
  name: "upload-content",
  data() {
    return {
      text_content: "",
      text_title: "",
      progress: 0,
      texts: []
    };
  },
  computed: {
    isTextInputsNotEmpty() {
      return this.text_content.length > 0 && this.text_title.length > 0;
    }
  },
  methods: {
    async upload() {
      this.$modal.show("load-bar");
      let sizeInBytes = new Blob([this.text_content]).size;
      let sizeInMB = this.bytesToMegaBytes(sizeInBytes);
      if (sizeInMB > 0.5) {
        alert("Please reduce the size of text");
      } else {
        let load_response = await ApiService.upload(
          this.text_title,
          this.text_content
        );
        let load_message = this.handleResponse(load_response);
        if (load_message) {
          this.texts.push(load_message);
          this.findSimilar(load_message.id);
        }
      }
      this.$modal.hide("load-bar");
    },
    findSimilar(textId) {
      this.$router.push({ path: `/compare/${textId}` });
    },
    bytesToMegaBytes(bytes) {
      return bytes / (1024 * 1024);
    }
  },
  async mounted() {
    let textsResponse = await ApiService.getTexts();
    let textsMessage = this.handleResponse(textsResponse);
    if (textsMessage) this.texts = textsMessage;
  }
};
</script>

<style scoped>
textarea {
  margin: 0px 0px;
  padding: 5px;
  min-height: 16px;
  line-height: 16px;
  width: 100%;
  height: calc(100vh - 20px);
  display: block;
  margin: 0px auto;
}
#text_title {
  width: 100%;
}
</style>
