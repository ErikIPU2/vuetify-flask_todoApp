<template>
  <div>
    <v-app v-if="initialLoading">
      <v-content name="content">
        <v-container fill-height align-center justify-center>
          <div class="text-center">
            <v-progress-circular indeterminate color="accent" size="150" width="5">Carregando...</v-progress-circular>
          </div>
        </v-container>
      </v-content>
    </v-app>
    <v-app v-else>
      <v-app-bar color="primary" class="white--text" app hide-on-scroll>
        <v-toolbar-title>Lista de tarefas</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn @click="loadTodos" icon class="white--text">
          <v-icon>mdi-reload mdi-spin</v-icon>
        </v-btn>
        <v-btn @click="logout" icon class="white--text">
          <v-icon>mdi-logout</v-icon>
        </v-btn>
      </v-app-bar>
      <v-content>
        <v-container>
          <v-btn fab dark large color="accent" fixed right bottom @click="openTodoCreate">
            <v-icon dark>mdi-plus</v-icon>
          </v-btn>
          <div>
            <Todo
              v-for="(todo, key) in todos"
              :key="key"
              :title="todo.title"
              :description="todo.description"
              :id="todo.id"
              :priority="todo.priority"
              :isDone="todo.isDone"
              :updateDoneUrl="apiUrl+'/todo'"
              color="secondary"
            ></Todo>
            <v-divider></v-divider>
            <transition name="fade">
              <Todo
                creationMode
                v-model="createTodoVisible"
                :createPostUrl="apiUrl+'/todo'"
                @created="loadTodos"
                color="secondary"
              />
            </transition>
          </div>
        </v-container>
      </v-content>
    </v-app>
  </div>
</template>

<script>
import axios from "axios";
import Todo from "../components/Todo";

export default {
  name: "Main",
  components: {
    Todo
  },

  data() {
    return {
      apiUrl: "http://127.0.0.1:5000/api",

      drawer: false,

      initialLoading: true,
      user: {
        username: null,
        user_id: null
      },

      todos: [],

      createTodoVisible: false
    };
  },

  created() {
    axios
      .get(`${this.apiUrl}/session`, { withCredentials: true })
      .then(res => {
        if (res.data.status) {
          this.user.username = res.data.username;
          this.user.user_id = res.data.user_id;

          this.loadTodos();
        } else {
          alert("Você precisa estar logado para fazer isso");
          window.location.href = "/#/login";
        }
      })
      .catch(res => {
        window.location.href = "/#/login";
      })
      .finally(res => {
        this.initialLoading = false;
      });
  },

  methods: {
    logout() {
      axios
        .get(`${this.apiUrl}/session/logout`, { withCredentials: true })
        .finally(res => {
          window.location.href = "/#/login";
        });
    },

    loadTodos() {
      axios.get(`${this.apiUrl}/todo`, { withCredentials: true }).then(res => {
        if (res.data.status) {
          this.todos = res.data.data;
        }
      });
    },

    openTodoCreate() {
      this.createTodoVisible = true;
      window.scrollTo(0, document.body.scrollHeight);
    }
  }
};
</script>

<style>
</style>