import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OrchestrationStateService } from '../../services/orchestration-state.service';
import { DeploymentMode, OperatingSystem, UserPersona } from '../../types/orchestration';

@Component({
  standalone: true,
  selector: 'app-header',
  imports: [CommonModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
})
export class HeaderComponent {
  modes: { value: DeploymentMode; label: string }[] = [
    { value: 'kubernetes', label: 'Kubernetes' },
    { value: 'docker-compose', label: 'Docker Compose' },
    { value: 'bare-metal', label: 'Bare-Metal' },
  ];

  osTargets: { value: OperatingSystem; label: string; icon: string }[] = [
    { value: 'all', label: 'All', icon: '🌐' },
    { value: 'linux', label: 'Linux', icon: '🐧' },
    { value: 'windows', label: 'Windows', icon: '🪟' },
    { value: 'macos', label: 'macOS', icon: '🍏' },
  ];

  personas: { value: UserPersona; label: string }[] = [
    { value: 'platform-admin', label: 'Admin' },
    { value: 'developer', label: 'Developer' },
    { value: 'auditor', label: 'Auditor' },
  ];

  tabs: Array<{ value: 'overview' | 'telemetry' | 'create'; label: string }> = [
    { value: 'overview', label: 'Overview' },
    { value: 'telemetry', label: 'Telemetry' },
    { value: 'create', label: 'Create App' },
  ];

  constructor(public state: OrchestrationStateService) {}

  get personaValue(): UserPersona {
    return this.state.persona$.value;
  }

  get canEditMode(): boolean {
    return this.personaValue === 'platform-admin';
  }

  setActiveTab(value: 'overview' | 'telemetry' | 'create') {
    this.state.setActiveTab(value);
  }
}
