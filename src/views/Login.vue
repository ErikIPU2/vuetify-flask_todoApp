<template>
  <v-app>
    <v-content name="content">
      <v-container fill-height>
        <v-layout align-center justify-center row>
          <v-flex sm12 md5>
            <v-card class="mx-auto" :loading="cardLoading">
              <v-toolbar flat>
                <v-toolbar-title>{{ getIsSignUpString }}</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-toolbar-items>
                  <v-btn elevation="1" @click="changeFormMethod" text>{{ getReverseIsSignUpString }}</v-btn>
                </v-toolbar-items>
              </v-toolbar>

              <v-img src="https://source.unsplash.com/random" height="200px">
                <v-card-title class="align-end fill-height white--text">Bem vindo!</v-card-title>
              </v-img>

              <v-card-text>
                <v-alert
                  v-model="errorAlert"
                  type="error"
                  border="left"
                  dismissible
                  colored-border
                >{{ errorAlertMessage }}</v-alert>
                <v-form ref="form" v-model="formValid">
                  <v-text-field
                    v-model="inputsValues.username"
                    :rules="inputsRules.usernameRules"
                    required
                    label="Nome de Usuario"
                    prepend-icon="mdi-account-circle mdi-spin"
                  ></v-text-field>
                  <v-text-field
                    v-model="inputsValues.password"
                    :rules="inputsRules.passwordRules"
                    required
                    label="Senha"
                    type="password"
                    prepend-icon="mdi-lock"
                  ></v-text-field>
                </v-form>
              </v-card-text>

              <v-card-actions>
                <v-btn
                  :disabled="!formValid"
                  block
                  @click="formSubmit"
                  color="accent"
                >{{ getIsSignUpString }}</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",

  data() {
    return {
      apiUrl: "http://127.0.0.1:5000/api",
      api: axios.create({
        withCredentials: true
      }),

      isSignUp: false,

      inputsValues: {
        username: "",
        password: ""
      },

      formValid: true,

      errorAlert: false,
      errorAlertMessage: "",

      cardLoading: false,

      inputsRules: {
        usernameRules: [
          value => !!value || "Você precisa digitar o seu nome de usuario"
        ],
        passwordRules: [value => !!value || "Você precisa digitar a sua senha"]
      }
    };
  },

  methods: {
    changeFormMethod() {
      this.isSignUp = !this.isSignUp;
    },

    formSubmit() {
      if (this.isSignUp) {
        this.signup();
      } else {
        this.login();
      }
    },

    login() {
      if (this.$refs.form.validate()) {
        const bodyForm = new FormData();
        bodyForm.set("username", this.inputsValues.username);
        bodyForm.set("password", this.inputsValues.password);
        this.cardLoading = true;
        this.api
          .post(`${this.apiUrl}/session/login`, bodyForm, {
            withCredentials: true
          })
          .then(res => {
            if (res.status == 200) {
              if (res.data.status) {
                window.location.href = "/";
              } else {
                this.errorAlert = true;
                this.errorAlertMessage = "Usuario ou senha incorreto";
              }
            }
          })
          .finally(res => {
            this.cardLoading = false;
          });
      }
    },

    signup() {
      if (this.$refs.form.validate()) {
        const bodyForm = new FormData();
        bodyForm.set("username", this.inputsValues.username);
        bodyForm.set("password", this.inputsValues.password);
        this.cardLoading = true;
        this.api
          .post(`${this.apiUrl}/session/signup`, bodyForm)
          .then(res => {
            if (res.data.status) {
              window.location.href = "/";
            } else {
              this.errorAlert = true;
              this.errorAlertMessage = "Nome de usuario já existe";
            }
          })
          .finally(res => {
            this.cardLoading = false;
          });
      }
    }
  },

  computed: {
    getIsSignUpString() {
      if (this.isSignUp) {
        return "Cadastrar";
      } else {
        return "Login";
      }
    },

    getReverseIsSignUpString() {
      if (!this.isSignUp) {
        return "Cadastrar";
      } else {
        return "Login";
      }
    }
  }
};
</script>
