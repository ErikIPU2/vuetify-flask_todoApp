<template>
  <v-layout>
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
            <v-btn icon>
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
            <v-btn @click="createTodo" color="secondary">Criar Tarefa</v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
      <v-card color="primary" class="white--text my-2" hover v-else>
        <v-card-title>
          <span>{{ title }}</span>
          <v-spacer></v-spacer>
          <v-checkbox color="accent" v-model="done"></v-checkbox>
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
    "isDone",
    "creationMode",
    "createPostUrl"
  ],

  created() {
    this.done = this.isDone;
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
              console.log(res);
            }
          })
          .catch(res => {
            alert("Ocorreu algum erro");
            console.error(res);
          });
      }
    }
  }
};
</script>

<style>
</style> 