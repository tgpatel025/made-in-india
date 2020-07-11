import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { GlobalSharedModule } from '../../shared/modules/global-shared/global-shared.module';
import { SearchResultsComponent } from './components/search-results/search-results.component';



@NgModule({
  declarations: [
    DashboardComponent,
    SearchResultsComponent
  ],
  imports: [
    CommonModule,
    GlobalSharedModule
  ],
  exports: [
    DashboardComponent,
    SearchResultsComponent
  ]
})
export class HomeModule { }
