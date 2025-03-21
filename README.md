# Central Brain Backend

Backend API service for the Central Brain application.

## Environment Variables

The following environment variables are required:

```
MONGODB_URI=your_mongodb_connection_string
PORT=3000
JWT_SECRET=your_jwt_secret
```

## Development

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

## Production

The service is configured to deploy on Render.com. Required environment variables must be set in the Render dashboard. 