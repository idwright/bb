import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';

import { AppComponent }  from './app.component';
import { DashboardComponent }   from './dashboard.component';
import { EntityDetailComponent } from './entity-detail.component';
import { EntitiesComponent }      from './entities.component';
import { EntityApi }          from './typescript-angular2-client/api/EntityApi';
import { HeroService }          from './hero.service';

import { AppRoutingModule }     from './app-routing.module';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule
  ],
  declarations: [
    AppComponent,
    DashboardComponent,
    EntityDetailComponent,
    EntitiesComponent
  ],
  providers: [ 
  EntityApi,
  HeroService
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }

