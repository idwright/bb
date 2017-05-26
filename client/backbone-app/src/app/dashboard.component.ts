import { Component, OnInit } from '@angular/core';

import { Entities } from './typescript-angular2-client/model/Entities';

import { EntityApi } from './typescript-angular2-client/api/EntityApi';

@Component({
  selector: 'my-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {

  entities: Entities;

  constructor(private entityApi: EntityApi) { }

  ngOnInit(): void {
    this.entityApi.downloadEntitiesByProperty("sample_type", "DNAC")
    .subscribe(
    (entities) => {
                    console.log(entities);
                    this.entities = entities;
                },
                (err) => console.log(err),
                () => { console.log("Downloaded entities") }
                );
  }
}
