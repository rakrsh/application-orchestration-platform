import { Component } from '@angular/core';
import { trace } from '@opentelemetry/api';
import { Application } from './types/orchestration';
import { OrchestrationStateService } from './services/orchestration-state.service';

const tracer = trace.getTracer('aop-frontend');

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: false,
})
export class AppComponent {
  applications: Application[] = [
    {
      id: 'app-01',
      name: 'E-Commerce Platform',
      description: 'Checkout workflow, catalog delivery, and payment orchestration.',
      environment: 'production',
      status: 'healthy',
      tags: ['linux', 'windows'],
      createdAt: '2026-07-21T14:20:00Z',
      projects: [
        {
          id: 'proj-01',
          name: 'auth-api',
          appId: 'app-01',
          osTarget: 'linux',
          runtime: 'Node.js 20',
          status: 'healthy',
          replicas: 3,
          targetReplicas: 4,
          cpuLimitRatio: 0.65,
          memoryUsageMb: 540,
          latencyP95Ms: 120,
          throughputRps: 140,
          errorRatePercent: 0.8,
          lastDeployedAt: '2026-07-31T09:45:00Z',
        },
        {
          id: 'proj-02',
          name: 'payment-worker',
          appId: 'app-01',
          osTarget: 'windows',
          runtime: 'Python 3.12',
          status: 'degraded',
          replicas: 2,
          targetReplicas: 2,
          cpuLimitRatio: 0.72,
          memoryUsageMb: 620,
          latencyP95Ms: 210,
          throughputRps: 72,
          errorRatePercent: 1.9,
          lastDeployedAt: '2026-07-31T10:12:00Z',
        },
      ],
    },
  ];

  constructor(public state: OrchestrationStateService) {
    tracer.startActiveSpan('dashboard.initialized', (span) => {
      span.setAttribute('app.name', 'application-orchestration-platform');
      span.end();
    });
  }
}
