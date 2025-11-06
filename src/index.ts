// src/index.ts
import express from 'express';
import bodyParser from 'body-parser';
import { routes } from './routes/index';
import { config } from './config/index';

const app = express();
const PORT = config.port || 3000;

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Routes
app.use('/api', routes);

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});