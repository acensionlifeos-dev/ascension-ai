/**
 * Permissions Routes - Check and grant permissions for AP capabilities
 */

import { Router, Request, Response } from 'express';
import {
  getRequiredPermissions,
  grantPermission,
  requestPermissions,
  PermissionStatus
} from '../services/permission-engine';
import { AuthRequest } from '../middleware/auth';

const router = Router();

/**
 * GET /api/v1/permissions/:capabilityId
 * What permissions are needed for a capability
 */
router.get('/:capabilityId', (req: AuthRequest, res: Response) => {
  const scopes = getRequiredPermissions(req.params.capabilityId);
  res.json({ capability: req.params.capabilityId, permissions: scopes });
});

/**
 * POST /api/v1/permissions/check
 * Body: { capabilityId, permissions: { id: { granted: bool } } }
 * Returns what is missing and what AP can do
 */
router.post('/check', (req: AuthRequest, res: Response) => {
  const { capabilityId, permissions = {} } = req.body;
  
  if (!capabilityId) {
    return res.status(400).json({ error: 'capabilityId required' });
  }
  
  const request = requestPermissions(capabilityId, permissions as Record<string, PermissionStatus>);
  res.json(request);
});

/**
 * POST /api/v1/permissions/grant
 * Body: { permissionId, conditions?: string[] }
 */
router.post('/grant', (req: AuthRequest, res: Response) => {
  const { permissionId, conditions } = req.body;
  
  if (!permissionId) {
    return res.status(400).json({ error: 'permissionId required' });
  }
  
  const status = grantPermission(permissionId, {}, conditions);
  res.json({ granted: status });
});

export default router;
