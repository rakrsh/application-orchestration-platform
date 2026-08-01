import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-replica-slider',
  templateUrl: './replica-slider.component.html',
  styleUrls: ['./replica-slider.component.css']
})
export class ReplicaSliderComponent {
  @Input() value = 1;
  @Input() min = 1;
  @Input() max = 20;
  @Input() disabled = false;
  @Output() valueChange = new EventEmitter<number>();
  @Output() commit = new EventEmitter<number>();

  get estimatedRam() {
    return Math.round(this.value * 220 + 180);
  }

  get estimatedCpu() {
    return (this.value * 0.12 + 0.1).toFixed(2);
  }

  onInput(event: Event) {
    const newValue = Number((event.target as HTMLInputElement).value);
    this.value = newValue;
    this.valueChange.emit(newValue);
  }

  onChange() {
    this.commit.emit(this.value);
  }
}
