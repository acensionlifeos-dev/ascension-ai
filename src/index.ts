/**
 * Express Server - Ascension AI API
 */

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import path from 'path';
import { authMiddleware } from './middleware/auth';
import { chatRoutes } from './routes/chat';
import { capabilityRoutes } from './routes/capabilities';
import { usageRoutes } from './routes/usage';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(compression());
app.use(express.json());

// Serve static files
app.use(express.static(path.join(__dirname, '../public')));

// Routes
app.use('/api/v1/chat', authMiddleware, chatRoutes);
app.use('/api/v1/capabilities', authMiddleware, capabilityRoutes);
app.use('/api/v1/usage', authMiddleware, usageRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start server
app.listen(PORT, () => {
  console.log(`Ascension AI API running on port ${PORT}`);
});

export default app;
