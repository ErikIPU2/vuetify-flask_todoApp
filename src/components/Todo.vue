<template>
  <v-layout v-if="$attrs.value || showFlag">
    <v-flex>
      <v-card class="white--text my-2" hover v-if="creationMode === ''">
        <v-form ref="form" v-model="formValid">
          <v-card-title>
            <v-text-field
              v-model="create.title"
              required
              :rules="createRules.titleRules"
              label="Titulo"
            ></v-text-field>
            <v-spacer></v-spacer>
            <v-btn icon @click="close">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-textarea
              flat
              rows="1"
              auto-grow
              required
              :rules="createRules.descriptionRules"
              label="Descrição"
              v-model="create.description"
            ></v-textarea>
          </v-card-text>
          <v-card-actions>
            <v-radio-group
              v-model="create.priority"
              :column="$vuetify.breakpoint.smAndDown ? true:false"
            >
              <v-radio v-for="n in 3" :key="n" :label="prioritysName[n-1]"></v-radio>
            </v-radio-group>
            <v-spacer></v-spacer>
            <v-btn @click="createTodo" :color="color">Criar Tarefa</v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
      <v-card :color="color" class="white--text my-2" hover v-else>
        <v-card-title>
          <span>{{ title }}</span>
          <v-spacer></v-spacer>
          <v-checkbox color="accent" v-model="done" @change="updateTodo"></v-checkbox>
        </v-card-title>
        <v-card-text class="white--text">{{ description }}</v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from "axios";

export default {
  name: "Todo",
  props: [
    "title",
    "description",
    "id",
    "priority",
    "isDone",
    "creationMode",
    "createPostUrl",
    "updateDoneUrl",
    "color"
  ],

  created() {
    this.done = this.isDone;

    if (this.$attrs.value === undefined) {
      this.showFlag = true;
    }
  },

  data() {
    return {
      done: null,

      formValid: true,

      prioritysName: ["baixa", "media", "alta"],

      create: {
        title: "",
        description: "",
        priority: 0
      },

      showFlag: false,

      createRules: {
        titleRules: [values => !!values || "Você precisa digitar o titulo"],
        descriptionRules: [
          values => !!values || "Você precisa digitar a descrição"
        ]
      }
    };
  },

  methods: {
    createTodo() {
      if (this.$refs.form.validate()) {
        const bodyForm = new FormData();
        bodyForm.set("title", this.create.title);
        bodyForm.set("description", this.create.description);
        bodyForm.set("priority", this.create.priority);
        axios
          .post(`${this.createPostUrl}`, bodyForm, { withCredentials: true })
          .then(res => {
            if (res.data.status) {
              this.$emit("created");
              this.close();
            }
          })
          .catch(res => {
            alert("Ocorreu algum erro");
            console.error(res);
          });
      }
    },

    updateTodo() {
      const bodyForm = new FormData();
      bodyForm.set("title", this.title);
      bodyForm.set("description", this.description);
      bodyForm.set("priority", this.priority);
      bodyForm.set("isDone", this.done);
      bodyForm.set("id", this.id);
      axios
        .put(`${this.updateDoneUrl}`, bodyForm, { withCredentials: true })
        .then(res => {
          this.$emit("update")
        })
        .catch(res => {
          alert("Ocorreu algum erro");
          console.error(res);
        });
    },

    close() {
      this.$emit("input", false);
      this.create.title = "";
      this.create.description = "";
      this.create.priority = 0;
    }
  }
};
</script>

<style>
</style> 