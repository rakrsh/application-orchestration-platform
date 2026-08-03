import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface TelemetryTrace {
  id: string;
  operation: string;
  durationMs: number;
  status: 'ok' | 'error';
  timestamp: string;
  service: string;
}

export interface TelemetryResource {
  name: string;
  type: string;
  state: string;
  health: string;
  cpuPercent: number;
  memoryMb: number;
  endpoints: string[];
}

export interface TelemetryPayload {
  jaeger: {
    service: string;
    traceCount: number;
    latencyP95Ms: number;
    traces: TelemetryTrace[];
  };
  aspire: {
    dashboard: string;
    healthScore: number;
    resources: TelemetryResource[];
    alerts: string[];
  };
}

@Injectable({
  providedIn: 'root',
})
export class TelemetryService {
  constructor(private http: HttpClient) {}

  getTelemetry(): Observable<TelemetryPayload> {
    return this.http.get<TelemetryPayload>('/api/telemetry');
  }
}
