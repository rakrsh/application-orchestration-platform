import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
import { HeaderComponent } from './components/layout/header.component';
import { OverviewTabComponent } from './components/dashboard/overview-tab.component';
import { ApplicationCardComponent } from './components/dashboard/application-card.component';
import { ProjectCardComponent } from './components/dashboard/project-card.component';
import { ReplicaSliderComponent } from './components/dashboard/replica-slider.component';
import { CreateAppWizardComponent } from './components/dashboard/create-app-wizard.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    OverviewTabComponent,
    ApplicationCardComponent,
    ProjectCardComponent,
    ReplicaSliderComponent,
    CreateAppWizardComponent
  ],
  imports: [BrowserModule, FormsModule],
  bootstrap: [AppComponent]
})
export class AppModule {}
