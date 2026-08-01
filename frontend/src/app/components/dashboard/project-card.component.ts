import { Component, EventEmitter, Input, Output } from '@angular/core';
import { DeploymentMode, OperatingSystem, ProjectService, UserPersona } from '../../types/orchestration';

@Component({
  selector: 'app-project-card',
  templateUrl: './project-card.component.html',
  styleUrls: ['./project-card.component.css']
})
export class ProjectCardComponent {
  @Input() project!: ProjectService;
  @Input() deploymentMode: DeploymentMode = 'kubernetes';
  @Input() persona: UserPersona = 'platform-admin';
  @Input() canEdit = true;
  @Output() replicaCommit = new EventEmitter<number>();

  get deploymentLabel(): string {
    switch (this.deploymentMode) {
      case 'docker-compose':
        return 'Container';
      case 'bare-metal':
        return 'Service';
      default:
        return 'Pod';
    }
  }

  handleReplicaCommit(value: number) {
    if (this.canEdit) {
      this.replicaCommit.emit(value);
    }
  }
}
