import { Component, OnInit } from '@angular/core';

import * as models from './typescript-angular2-client/model/models';

import { EntityApi } from './typescript-angular2-client/api/EntityApi';

@Component({
  selector: 'my-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {

  entities: InlineResponse201[] = [];

  constructor(private entityApi: EntityApi) { }

  ngOnInit(): void {
    this.entityApi.downloadEntitiesByProperty("test1", "DNAC")
    .subscribe(
                (entities) => {
                    this.entities = entities;
                },
                (err) => console.log(err),
                () => { console.log("Downloaded entities") }
                );
  }
}
