import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { GlobalSharedModule } from 'src/app/shared/modules/global-shared/global-shared.module';



@NgModule({
  declarations: [
    DashboardComponent
  ],
  imports: [
    CommonModule,
    GlobalSharedModule
  ],
  exports: [
    DashboardComponent
  ]
})
export class HomeModule { }
