/**
 * Capabilities Routes - List and query capabilities
 */

import { Router, Response } from 'express';
import { getAllCapabilities, getCapabilityById, getCapabilitiesByCategory } from '../services/capability-registry';
import { AuthRequest } from '../middleware/auth';

const router = Router();

/**
 * GET /api/v1/capabilities
 * Get all capabilities
 */
router.get('/', (req: AuthRequest, res: Response) => {
  const capabilities = getAllCapabilities();
  res.json({ capabilities });
});

/**
 * GET /api/v1/capabilities/category/:category
 * Get capabilities by category (must come before /:id)
 */
router.get('/category/:category', (req: AuthRequest, res: Response) => {
  const capabilities = getCapabilitiesByCategory(req.params.category);
  res.json({ capabilities });
});

/**
 * GET /api/v1/capabilities/:id
 * Get specific capability
 */
router.get('/:id', (req: AuthRequest, res: Response) => {
  const capability = getCapabilityById(req.params.id);
  
  if (!capability) {
    return res.status(404).json({ error: 'Capability not found' });
  }
  
  res.json({ capability });
});

export default router;
