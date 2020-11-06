<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Words</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-on:click="Listen">Listen</button>
        <br><br>
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
  },
  created() {
    this.getWords();
  },
};
</script>
