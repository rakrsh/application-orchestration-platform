import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  Application,
  OperatingSystem,
  DeploymentMode,
  UserPersona,
} from '../../types/orchestration';
import { ApplicationCardComponent } from './application-card.component';

@Component({
  standalone: true,
  selector: 'app-overview-tab',
  imports: [CommonModule, ApplicationCardComponent],
  templateUrl: './overview-tab.component.html',
  styleUrls: ['./overview-tab.component.css'],
})
export class OverviewTabComponent {
  @Input() applications: Application[] = [];
  @Input() osFilter: OperatingSystem = 'all';
  @Input() deploymentMode: DeploymentMode = 'kubernetes';
  @Input() persona: UserPersona = 'platform-admin';

  get filteredApplications(): Application[] {
    if (this.osFilter === 'all') {
      return this.applications;
    }

    return this.applications.filter((app) =>
      app.projects.some((project) => project.osTarget === this.osFilter)
    );
  }
}
