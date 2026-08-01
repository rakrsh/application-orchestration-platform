import { Component, Input } from '@angular/core';
import { Application, DeploymentMode, OperatingSystem, UserPersona, ProjectService } from '../../types/orchestration';

@Component({
  selector: 'app-application-card',
  templateUrl: './application-card.component.html',
  styleUrls: ['./application-card.component.css']
})
export class ApplicationCardComponent {
  @Input() application!: Application;
  @Input() osFilter: OperatingSystem = 'all';
  @Input() deploymentMode: DeploymentMode = 'kubernetes';
  @Input() persona: UserPersona = 'platform-admin';

  expanded = false;

  get projectCount(): number {
    return this.filteredProjects.length;
  }

  get filteredProjects(): ProjectService[] {
    if (this.osFilter === 'all') {
      return this.application.projects;
    }
    return this.application.projects.filter(project => project.osTarget === this.osFilter);
  }

  get aggregatedCpu(): string {
    const total = this.filteredProjects.reduce((sum, project) => sum + project.cpuLimitRatio, 0);
    return `${Math.round((total / Math.max(this.filteredProjects.length, 1)) * 100)}%`;
  }

  get aggregatedMemory(): string {
    const total = this.filteredProjects.reduce((sum, project) => sum + project.memoryUsageMb, 0);
    return `${Math.round(total)} MB`;
  }

  toggleExpand() {
    this.expanded = !this.expanded;
  }

  formatStatus(status: string) {
    switch (status) {
      case 'healthy':
        return 'Healthy';
      case 'degraded':
        return 'Degraded';
      case 'failed':
        return 'Failed';
      default:
        return status;
    }
  }
}
