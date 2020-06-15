<template>
  <div>
    <router-link to="/upload">&lt;- Back to upload</router-link>
    <div class="row">
      <div class="col-4">
        <div class="card">
          <div class="card-header">Similar lines</div>
          <ul class="'list-group list-group-flush'">
            <li class="list-group-item" v-for="(similarText, index) in similarTexts" :key="index">
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
            <paginate
              name="paginatedTextLines"
              :list="textLines"
              :per="50"
              :class="'list-group list-group-flush'"
            >
              <p v-for="(textline, index) in paginated('paginatedTextLines')" :key="index">
                <a :href="textline.id" @click.prevent="compare(textline.id)">{{ textline.line }}</a>
              </p>
            </paginate>
            <div class="row">
              <div class="col-4"></div>
              <div class="col-4">
                <paginate-links
                  for="paginatedTextLines"
                  :async="true"
                  :show-step-links="true"
                  :step-links="{ next: 'Next', prev: 'Previous' }"
                  :classes="{ 'ul': 'pagination', 'li': 'page-item', 'a': 'page-link'}"
                  :hide-single-page="true"
                ></paginate-links>
              </div>
              <div class="col-4"></div>
            </div>
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
      similarTexts: [],
      textId: this.$route.params.textId,
      paginate: ["paginatedTextLines"]
    };
  },
  computed: {},
  methods: {
    async compare(lineId) {
      this.$modal.show("load-bar");
      try {
        let similarTextResponse = await ApiService.getSimilarLines(lineId);
        let similarTextMessage = this.handleResponse(similarTextResponse);
        if (similarTextResponse) this.similarTexts = similarTextMessage;
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
