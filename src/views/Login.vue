<template>
  <v-app>
    <v-content name="content">
      <v-container fill-height>
        <v-layout align-center justify-center row>
          <v-flex sm12 md5>
            <v-card class="mx-auto">
              <v-toolbar flat>
                <v-toolbar-title>{{ getIsSignUpString }}</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-toolbar-items>
                  <v-btn @click="changeFormMethod" text>{{ getReverseIsSignUpString }}</v-btn>
                </v-toolbar-items>
              </v-toolbar>

              <v-img src="https://source.unsplash.com/random" height="200px">
                <v-card-title class="align-end fill-height white--text">Bem vindo!</v-card-title>
              </v-img>

              <v-card-text>
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
              </v-card-text>

              <v-card-actions>
                <v-btn block color="accent">{{ getIsSignUpString }}</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: "Login",

  data() {
    return {
      isSignUp: false,

      inputsValues: {
        username: "",
        password: ""
      },

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
