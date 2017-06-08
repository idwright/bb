import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent }   from './dashboard/dashboard.component';
import { EntitiesComponent }      from './entities/entities.component';
import { EntitiesListComponent }      from './entities-list/entities-list.component';
import { EntityDetailComponent }  from './entity-detail/entity-detail.component';
import { SourceSummaryComponent }  from './source-summary/source-summary.component';
import { SourcePropertySummaryComponent }  from './source-property-summary/source-property-summary.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard',  component: DashboardComponent },
  { path: 'detail/:entityId', component: EntityDetailComponent },
  { path: 'sourceSummary/:sourceId', component: SourceSummaryComponent },
  { path: 'sourcePropertySummary/:sourceId/:propertyName', component: SourcePropertySummaryComponent },
  { path: 'list/:sourceId/:propertyName/:propertyValue', component: EntitiesListComponent },
  { path: 'entities',     component: EntitiesComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
