import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { DeploymentMode, OperatingSystem, UserPersona } from '../types/orchestration';

@Injectable({
  providedIn: 'root'
})
export class OrchestrationStateService {
  deploymentMode$ = new BehaviorSubject<DeploymentMode>('kubernetes');
  osFilter$ = new BehaviorSubject<OperatingSystem>('all');
  persona$ = new BehaviorSubject<UserPersona>('platform-admin');
  activeTab$ = new BehaviorSubject<'overview' | 'telemetry' | 'create'>('overview');

  setDeploymentMode(value: DeploymentMode) {
    if (this.persona$.value !== 'platform-admin') {
      return;
    }
    this.deploymentMode$.next(value);
  }

  setOsFilter(value: OperatingSystem) {
    this.osFilter$.next(value);
  }

  setPersona(value: UserPersona) {
    this.persona$.next(value);
  }

  setActiveTab(value: 'overview' | 'telemetry' | 'create') {
    this.activeTab$.next(value);
  }
}
