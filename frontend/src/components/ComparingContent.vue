<template>
  <div>
    <router-link to="/upload">&lt;- Back to upload</router-link>
    <div class="row">
      <div class="col-4">
        <div class="card">
          <div class="card-header">Similar lines</div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item" v-for="(similarText, index) in similar_texts" :key="index">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">{{ similarText.text_name }}</h5>
                  <p class="card-text">{{ similarText.line }}</p>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
      <div class="col-8">
        <div class="card">
          <div class="card-header">Text content</div>
          <div class="card-body">
            <p v-for="(textline, index) in textLines" :key="index">
              <a :href="textline.id" @click.prevent="compare(textline.id)">{{ textline.line }}</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from "../services/ApiService";
import responseMixin from "../mixins/responseMixin";

export default {
  mixins: [responseMixin],
  name: "comparing-content",
  data() {
    return {
      textLines: [],
      similar_texts: [],
      textId: this.$route.params.textId
    };
  },
  computed: {},
  methods: {
    async compare(lineId) {
      this.$modal.show("load-bar");
      try {
        let similar_text_response = await ApiService.getSimilarLines(lineId);
        let similar_text_message = this.handleResponse(similar_text_response);
        if (similar_text_response) this.similar_texts = similar_text_message;
      } catch (error) {
        alert(error);
      } finally {
        this.$modal.hide("load-bar");
      }
    }
  },
  async mounted() {
    let responseTextLines = await ApiService.getTextLinesById(this.textId);
    this.textLines = this.handleResponse(responseTextLines);
  }
};
</script>
