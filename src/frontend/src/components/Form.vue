<template>
  <div class="container">
    <div class="row">
      <div class="progress" style="padding: 0">
        <div class="progress-bar" role="progressbar" :style="{width: progressValue + '%'}" v-bind:aria-valuenow="progressValue" aria-valuemin="0" aria-valuemax="100">
          {{ progressValue }}
        </div>
      </div>

      <form id="form-upload">
        <div class="mb-3">
          <label for="upload-url" class="form-label">Ссылка</label>
          <input v-model="url" v-on:change="checkOriginResolution()" type="text" class="form-control" id="upload-url" aria-describedby="upload-url-help">
          <div id="upload-url-help" class="form-text text-danger" v-bind:class="{ 'visible': isUrlError }">Заполните поле</div>
        </div>
        <div class="mb-3">
          <label for="select-original" class="form-label">Доступное исходное разрешение:</label>
          <select id="select-original" class="form-select" v-model="selectOriginalValue" v-bind:disabled="isSelectOriginalDisabled" v-on:change="checkResolution()">
            <option v-for="(item, index) in selectOriginal" :key="`item-${index}`">{{ item }}</option>
          </select>
          <div class="form-text">Введите ссылку для проверки доступного качества</div>
        </div>
        <div class="mb-3">
          <label for="select-final" class="form-label">Доступное конечное качество:</label>
          <select id="select-final" class="form-select" v-model="selectFinalValue" v-bind:disabled="isSelectFinalDisabled">
            <option v-for="(item, index) in selectFinal" :key="`item-${index}`">{{ item }}</option>
          </select>
          <div class="form-text">Введите качество для улучшения видео</div>
        </div>
        <button v-on:click="buttonSubmit()" type="button" class="btn btn-primary">{{ buttonText }}</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Form',
  data() {
    return {
      buttonText:          'Проверить качество',
      url:                 '',
      selectOriginalValue: '-',
      selectOriginal:      [
        '-'
      ],
      selectFinalValue:    '-',
      selectFinal:         [
        '-'
      ],

      isUrlError:               false,
      isSelectOriginalDisabled: true,
      isSelectFinalDisabled:    true,

      progressValue: '100'
    }
  },
  methods: {
    checkOriginResolution: function() {
      if (this.url.indexOf('https://www.youtube.com/watch?v=') + 1) {
        axios
            .post('/api/video_resolution', {
              url: this.url
            })
            .then(response => {
              this.selectOriginal           = response.data.data;
              this.isSelectOriginalDisabled = false;
              this.buttonText               = 'Улучшить видео';
            })
            .catch(error => {
              console.log(error);
            })
      }
    },
    checkFinalResolution:  function() {
      axios
          .post('/api/video_resolution_out', {
            resolution: this.selectOriginalValue
          })
          .then(response => {
            this.selectFinal           = response.data.data;
            this.isSelectFinalDisabled = false;
            this.buttonText            = 'Улучшить видео';
          })
          .catch(error => {
            console.log(error);
          })
    },
    buttonSubmit:          function() {
      axios
          .post('/api/create_video', {
            url:              this.url,
            quality_download: this.selectOriginalValue,
            quality_out:      this.selectFinalValue
          })
          .then(response => {
            this.selectOriginal           = response.data.data;
            this.isSelectOriginalDisabled = false;
            this.buttonText               = 'Улучшить видео';
          })
          .catch(error => {
            console.log(error);
          })
    },
    progressBar:           function() {
      setTimeout(function() {
        if (this.progressValue < 100) {
          axios
              .post('/api/progress_bar')
              .then(response => {
                this.progressValue = response.data.data;
              })
              .catch(error => {
                console.log(error);
              })
        } else {
          let is_finish = false;
          axios
              .post('/api/create_video_is_finish')
              .then(response => {
                is_finish = response.data.is_finish;
              })
              .catch(error => {
                console.log(error);
              })
          if (is_finish) {
            window.location.href = 'video';
          }
        }
      }, 1000);
    }
  }
}
</script>

<style scoped lang="sass">
body
  display: flex
  align-items: center
  padding-top: 40px
  padding-bottom: 40px
  background-color: #f5f5f5

#form-upload
  width: 100%
  max-width: 500px
  padding: 15px
  margin: auto

#upload-url-help
  visibility: hidden
</style>
