import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TelemetryService } from '../../services/telemetry.service';
import { TelemetryPayload } from '../../services/telemetry.service';

@Component({
  standalone: true,
  selector: 'app-telemetry-tab',
  imports: [CommonModule],
  templateUrl: './telemetry-tab.component.html',
  styleUrls: ['./telemetry-tab.component.css'],
})
export class TelemetryTabComponent implements OnInit {
  telemetry: TelemetryPayload | null = null;
  loading = true;

  constructor(private telemetryService: TelemetryService) {}

  ngOnInit(): void {
    this.telemetryService.getTelemetry().subscribe({
      next: (payload) => {
        this.telemetry = payload;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }
}
