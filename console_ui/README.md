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
