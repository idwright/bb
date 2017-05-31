import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent }  from './app.component';
import { DashboardComponent }   from './dashboard.component';
import { EntityDetailComponent } from './entity-detail.component';
import { EntityDetailFormComponent } from './entity-detail-form.component';
import { EntitiesListComponent }      from './entities-list.component';
import { EntitiesComponent }      from './entities.component';
import { SourceSummaryComponent }      from './source-summary.component';
import { SourcePropertySummaryComponent }      from './source-property-summary.component';
import { EntityApi }          from './typescript-angular2-client/api/EntityApi';
import { ReportApi }          from './typescript-angular2-client/api/ReportApi';
import { SourceApi }          from './typescript-angular2-client/api/SourceApi';

import { AppRoutingModule }     from './app-routing.module';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpModule
  ],
  declarations: [
    AppComponent,
    DashboardComponent,
    EntityDetailComponent,
    EntityDetailFormComponent,
    EntitiesListComponent,
    EntitiesComponent,
    SourceSummaryComponent,
    SourcePropertySummaryComponent,
  ],
  providers: [ 
  EntityApi,
  ReportApi,
  SourceApi,
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }

