# Console User interface

This folder contains the web user interface for the console of phiphi. The console allows users to configure a specific social media analyses.

## Available Scripts

### Running the development server.

```bash
    npm run dev
```

### Building for production.

```bash
    npm run build
```

### Running the production server.

```bash
    npm run start
```

### Linting

We have linting that works with pre commit and lint-staged. If you run `npm install` the pre
commit will automatically be installed and run on all staged files in `console_ui/`.

To run a lint check you can use the command:

```bash
  npm run lint
```

## Learn More

To learn more about **Refine**, please check out the [Documentation](https://refine.dev/docs)

- **REST Data Provider** [Docs](https://refine.dev/docs/core/providers/data-provider/#overview)
- **Mantine** [Docs](#)
- **Inferencer** [Docs](https://refine.dev/docs/packages/documentation/inferencer)

## Authentication for dev:

The default api that is configured in `phiphi/python/projects/phiphi` uses cookie based
authentication. This means that you can run the following code in the browser console to
authenticate as a user:

```
# Set the user email admin@admin.com is added by default.
document.cookie = "phiphi-user-email=admin@admin.com";

## Check have the correct users
fetch('http://localhost:8080/users/me', {
 method: 'GET',
 credentials: 'include'
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### Easy steps for Translation:

```
Simple way to translate:
Get required items to be translated in the proper json format and simply ask ChatGPT to translate the values(not the keys) to what ever language is required.

e.g: en ==> de

{
  "pages": {
        "login": {
            "title": "Sign in to your account",
            "signin": "Sign in",
            "signup": "Sign up",
            "divider": "or",
            "fields": {
                "email": "Email",
                "password": "Password"
            }
        }
    }
}

==>

{
  "pages": {
        "login": {
            "title": "Melden Sie sich bei Ihrem Konto an",
            "signin": "Einloggen",
            "signup": "Anmelden",
            "divider": "oder",
            "fields": {
                "email": "Email",
                "password": "Passwort"
            }
        }
  }
}
```

### Vercel documentation

```
1). Login to Vercel: Go to the Vercel website (vercel.com) and log in to your account.
2). Import Your Next.js Project: Once logged in, you'll see a button labeled "Import Project" on the dashboard. Click on it.
3). Choose The Git Repository: Select your Next.js project's Git repository from the list of available options.
4). Configure Deployment Settings: After selecting your repository, Vercel will present you with deployment settings. Choose the branch you want to deploy from, and configure any other settings you require, such as environment variables or build commands.
5). Deploy The Project: Once you've configured the settings, click on the "Deploy" button. Vercel will start the deployment process.
6). Monitor Deployment Progress: While your project is deploying, Vercel will show you the deployment progress in real-time. You can see which step of the deployment process it's currently on.
7). Access Your Deployed Next.js Application: Once the deployment is complete, Vercel will provide you with a unique URL where your Next.js application is hosted. You can click on this URL to access your deployed application.
```
