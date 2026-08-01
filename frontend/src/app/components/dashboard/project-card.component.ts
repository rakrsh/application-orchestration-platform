import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DeploymentMode, OperatingSystem, ProjectService, UserPersona } from '../../types/orchestration';
import { ReplicaSliderComponent } from './replica-slider.component';

@Component({
  standalone: true,
  selector: 'app-project-card',
  imports: [CommonModule, ReplicaSliderComponent],
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
