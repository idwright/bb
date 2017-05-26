import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent }  from './app.component';
import { DashboardComponent }   from './dashboard.component';
import { EntityDetailComponent } from './entity-detail.component';
import { EntityDetailFormComponent } from './entity-detail-form.component';
import { EntitiesComponent }      from './entities.component';
import { EntityApi }          from './typescript-angular2-client/api/EntityApi';

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
    EntitiesComponent
  ],
  providers: [ 
  EntityApi,
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }

