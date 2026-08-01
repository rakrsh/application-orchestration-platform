export type OperatingSystem = 'linux' | 'windows' | 'macos' | 'all';
export type DeploymentMode = 'kubernetes' | 'docker-compose' | 'bare-metal';
export type UserPersona = 'platform-admin' | 'developer' | 'auditor';
export type HealthStatus = 'healthy' | 'degraded' | 'failed' | 'provisioning' | 'stopped';

export interface OSNode {
  id: string;
  name: string;
  os: OperatingSystem;
  ip: string;
  cpuUsage: number;
  memoryUsage: number;
  status: 'online' | 'offline' | 'degraded';
  agentVersion: string;
}

export interface ProjectService {
  id: string;
  name: string;
  appId: string;
  osTarget: OperatingSystem;
  runtime: string;
  status: HealthStatus;
  replicas: number;
  targetReplicas: number;
  cpuLimitRatio: number;
  memoryUsageMb: number;
  latencyP95Ms: number;
  throughputRps: number;
  errorRatePercent: number;
  lastDeployedAt: string;
}

export interface Application {
  id: string;
  name: string;
  description: string;
  environment: 'production' | 'staging' | 'development';
  status: HealthStatus;
  projects: ProjectService[];
  tags: string[];
  createdAt: string;
}

export interface PlatformMetrics {
  activeNodesCount: number;
  totalCpuPercent: number;
  totalMemoryPercent: number;
  activeDeployments: number;
  globalErrorRate: number;
  p95LatencyMs: number;
}

export interface AppCreationPayload {
  name: string;
  description: string;
  environment: 'production' | 'staging' | 'development';
  importType: 'git' | 'zip';
  gitUrl?: string;
  gitBranch?: string;
  buildfilePath?: string;
  zipFile?: File | null;
  targetOs: OperatingSystem;
  detectedRuntime?: string;
  envVariables: Record<string, string>;
}
