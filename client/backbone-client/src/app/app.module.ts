import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppRoutingModule }     from './app-routing.module';

import { MaterialModule } from '@angular/material';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { NgxDatatableModule } from '@swimlane/ngx-datatable';
import 'hammerjs';

import { LeafletMarkerClusterModule } from '@asymmetrik/ngx-leaflet-markercluster';
import { LeafletModule } from '@asymmetrik/ngx-leaflet';

import { AppComponent } from './app.component';
import { EntitiesComponent } from './entities/entities.component';
import { EntitiesListComponent } from './entities-list/entities-list.component';
import { EntityDetailFormComponent } from './entity-detail-form/entity-detail-form.component';
import { SourceSummaryComponent } from './source-summary/source-summary.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { EntitiesDisplayComponent } from './entities-display/entities-display.component';
import { EntityDetailComponent } from './entity-detail/entity-detail.component';
import { SourcePropertySummaryComponent } from './source-property-summary/source-property-summary.component';
import { EntityApi }          from './typescript-angular2-client/api/EntityApi';
import { ReportApi }          from './typescript-angular2-client/api/ReportApi';
import { SourceApi }          from './typescript-angular2-client/api/SourceApi';
import { PropertyFormComponent } from './property-form/property-form.component';
import { AssocFormComponent } from './assoc-form/assoc-form.component';
import { PropertiesFormComponent } from './properties-form/properties-form.component';
import { EntitiesFullListComponent } from './entities-full-list/entities-full-list.component';
import { PropertiesSummaryComponent } from './properties-summary/properties-summary.component';
import { PropertySummaryComponent } from './property-summary/property-summary.component';
import { EntitiesByPropertyValueComponent } from './entities-by-property-value/entities-by-property-value.component';
import { EntitiesMapComponent } from './entities-map/entities-map.component';
import { AllEntitiesMapComponent } from './all-entities-map/all-entities-map.component';


@NgModule({
  declarations: [
    AppComponent,
    EntitiesComponent,
    EntitiesListComponent,
    EntityDetailFormComponent,
    SourceSummaryComponent,
    DashboardComponent,
    EntitiesDisplayComponent,
    EntityDetailComponent,
    SourcePropertySummaryComponent,
    PropertyFormComponent,
    AssocFormComponent,
    PropertiesFormComponent,
    EntitiesFullListComponent,
    PropertiesSummaryComponent,
    PropertySummaryComponent,
    EntitiesByPropertyValueComponent,
    EntitiesMapComponent,
    AllEntitiesMapComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    AppRoutingModule,
    MaterialModule,
    BrowserAnimationsModule,
    NgxDatatableModule,
    LeafletModule,
    LeafletMarkerClusterModule
  ],
  providers: [
      EntityApi,
      ReportApi,
      SourceApi,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
