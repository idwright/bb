import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AllEntitiesMapComponent } from './all-entities-map/all-entities-map.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { EntitiesComponent } from './entities/entities.component';
import { EntitiesFullListComponent } from './entities-full-list/entities-full-list.component';
import { EntitiesListComponent } from './entities-list/entities-list.component';
import { EntityDetailComponent } from './entity-detail/entity-detail.component';
import { PropertiesSummaryComponent } from './properties-summary/properties-summary.component';
import { PropertySummaryComponent } from './property-summary/property-summary.component';
import { EntitiesByPropertyValueComponent } from './entities-by-property-value/entities-by-property-value.component';
import { SourceSummaryComponent } from './source-summary/source-summary.component';
import { SourcePropertySummaryComponent } from './source-property-summary/source-property-summary.component';

const routes: Routes = [
  { path: '', redirectTo: '/full-list', pathMatch: 'full' },
  { path: 'full-map', component: AllEntitiesMapComponent },
  { path: 'full-list', component: EntitiesFullListComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'propertiesSummary', component: PropertiesSummaryComponent },
  { path: 'propertySummary/:propertyName', component: PropertySummaryComponent },
  { path: 'entitiesByPropValue/:propertyName/:propertyValue', component: EntitiesByPropertyValueComponent},
  { path: 'detail/:entityId', component: EntityDetailComponent },
  { path: 'sourceSummary/:sourceId', component: SourceSummaryComponent },
  { path: 'sourcePropertySummary/:sourceId/:propertyName', component: SourcePropertySummaryComponent },
  { path: 'list/:sourceId/:propertyName/:propertyValue', component: EntitiesListComponent },
  { path: 'entities', component: EntitiesComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
