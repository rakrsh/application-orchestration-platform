import { Component } from '@angular/core';
import { AppCreationPayload, OperatingSystem } from '../../types/orchestration';

@Component({
  selector: 'app-create-app-wizard',
  templateUrl: './create-app-wizard.component.html',
  styleUrls: ['./create-app-wizard.component.css']
})
export class CreateAppWizardComponent {
  activeStep: 'git' | 'zip' = 'git';
  payload: AppCreationPayload = {
    name: '',
    description: '',
    environment: 'development',
    importType: 'git',
    gitUrl: '',
    gitBranch: 'main',
    zipFile: null,
    targetOs: 'linux',
    detectedRuntime: undefined,
    envVariables: {}
  };
  dropMessage = 'Drag and drop a ZIP bundle here, or click to browse.';
  runtimeHint = '';
  envRows = [{ key: '', value: '' }];

  selectStep(step: 'git' | 'zip') {
    this.activeStep = step;
    this.payload.importType = step === 'git' ? 'git' : 'zip';
  }

  handleFileInput(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0] ?? null;
    this.processFile(file);
  }

  processFile(file: File | null) {
    if (!file) {
      this.payload.zipFile = null;
      this.dropMessage = 'Drag and drop a ZIP bundle here, or click to browse.';
      this.runtimeHint = '';
      return;
    }

    this.payload.zipFile = file;
    this.runtimeHint = 'Node.js 20 project detected with package.json';
    this.payload.detectedRuntime = 'Node.js 20';
    this.dropMessage = `${file.name} selected (${Math.round(file.size / 1024)} KB)`;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    const file = event.dataTransfer?.files?.[0] ?? null;
    this.processFile(file);
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
  }

  addEnvRow() {
    this.envRows.push({ key: '', value: '' });
  }

  removeEnvRow(index: number) {
    this.envRows.splice(index, 1);
    this.syncEnvVariables();
  }

  syncEnvVariables() {
    this.payload.envVariables = this.envRows.reduce((acc, row) => {
      if (row.key.trim()) {
        acc[row.key] = row.value;
      }
      return acc;
    }, {} as Record<string, string>);
  }

  onEnvKeyChange(index: number, value: string) {
    this.envRows[index].key = value;
    this.syncEnvVariables();
  }

  onEnvValueChange(index: number, value: string) {
    this.envRows[index].value = value;
    this.syncEnvVariables();
  }

  submit() {
    console.log('App creation payload', this.payload);
    alert('Create app simulation complete.');
  }
}
