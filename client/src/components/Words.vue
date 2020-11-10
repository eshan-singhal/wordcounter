<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Words</h1>
        <b-form @submit="onSubmitAddWord" class="w-100">
        <b-form-group id="form-add-group"
                      label-for="form-add-input">
            <b-form-input id="form-add-input"
                          type="text"
                          v-model="addWordForm.word"
                          required
                          placeholder="Enter word">
            </b-form-input>
          </b-form-group>
          <b-button-group>
            <b-button type="submit" variant="primary">Add</b-button>
          </b-button-group>
        </b-form>
        <b-form @submit="onSubmitSearchWord" class="w-100">
        <b-form-group id="form-search-group"
                      label-for="form-search-input">
            <b-form-input id="form-search-input"
                          type="text"
                          v-model="searchWordForm.word"
                          required
                          placeholder="Enter word">
            </b-form-input>
          <b-button-group>
            <b-button type="submit" variant="primary">Search</b-button>
          </b-button-group>
          </b-form-group>
        </b-form>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Word</th>
              <th scope="col">Frequency</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(word, index) in words" :key="index">
              <td>{{ word.word }}</td>
              <td>{{ word.frequency }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      words: [],
      addWordForm: {
        word: ''
      },
      searchWordForm: {
        word: ''
      }
    };
  },
  methods: {
    Listen() {
      const path = '/api/listen';
      axios.post(path)
        .then(() => {
          this.getWords();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
    getWords() {
      const path = '/api/frequent';
      axios.get(path)
        .then((res) => {
          this.words = res.data.words;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getSubstring(query) {
      const path = '/api/substring';
      axios.post(path, {
        sub: query
      })
        .then((res) => {
          // this.getWords();
          this.words = res.data.words;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addWord(word_to_add) {
      const path = '/api/add';
      axios.put(path, {
        word: word_to_add
      })
        .then(() => {
          this.getWords();
        })
    },
    onSubmitAddWord(evt) {
      evt.preventDefault();
      this.addWord(this.addWordForm.word);
      this.addWordForm.word = '';
    },
    onSubmitSearchWord(evt) {
      evt.preventDefault();
      this.getSubstring(this.searchWordForm.word);
      this.searchWordForm.word = '';
    }
  },
  created() {
    this.getWords();
  },
};
</script>
