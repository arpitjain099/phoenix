# Console User interface

This folder contains the web user interface for the console of Phoenix. The console allows users to
configure a specific social media analyses.

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

## Environment Variables:

The console UI uses `.env.<environment>` file to initialise the application with the correct config.

Currently there are 4 `.env.<environment>` files in use:

- `.env.example` and example file that can be used as a template for others
- `.env.local`
- `.env.development`
- `.env.production`

### Setup Environment Variables for Local Environment.

To set up environment variables, copy the .env.example file to create a new .env.local file:

```bash
    cp .env.example .env.local
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

The default api that is configured in `phoenix/python/projects/phiphi` uses cookie based
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

## Easy steps for Translation:

Simple way to translate:
Get required items to be translated in the proper json format and simply ask ChatGPT to translate the values (not the keys) to what ever language is required.

Example prompt:

Please translate the values in this JSON from English to <other language>. Check your work.

`/console_ui/public/locales/en/common.json`

## Deploying Your Next.js Project on Vercel:

1. **Login to Vercel:** - Visit [Vercel's website](https://vercel.com/) and log in to your account.

2. **Import Your Next.js Project:** - Once logged in, click on the "Import Project" button on the dashboard.

3. **Choose The Git Repository:** - Select your Next.js project's Git repository from the list.

4. **Configure Deployment Settings:** - Choose the branch you want to deploy from and configure other settings like environment variables.

5. **Deploy The Project:** - Click on the "Deploy" button to start the deployment process.

6. **Monitor Deployment Progress:** - Watch the real-time progress of your deployment on the Vercel dashboard.

7. **Access Your Deployed Application:** - Once deployment is complete, Vercel will provide a unique URL to access your Next.js application.

8. **Automatic Deployment:** - Vercel automatically deploys the application whenever changes are detected in the connected Git repository.

For more detailed instructions, refer to [Vercel's documentation](https://vercel.com/docs).
